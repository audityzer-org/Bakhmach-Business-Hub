// Bakhmach Business Hub - Investor Portal Authentication
// OAuth 2.0 + JWT + MFA Implementation

const express = require('express');
const jwt = require('jsonwebtoken');
const bcrypt = require('bcrypt');
const speakeasy = require('speakeasy');
const qrcode = require('qrcode');
const passport = require('passport');
const GoogleStrategy = require('passport-google-oauth20');

const router = express.Router();
const JWT_SECRET = process.env.JWT_SECRET || 'investor-portal-secret-key-2026';

// In-memory investor database (replace with DB)
const investors = new Map();
const sessions = new Map();
const mfaSecrets = new Map();

// Initialize Passport
passport.use(new GoogleStrategy({
    clientID: process.env.GOOGLE_CLIENT_ID,
    clientSecret: process.env.GOOGLE_CLIENT_SECRET,
    callbackURL: '/auth/google/callback'
  },
  (accessToken, refreshToken, profile, done) => {
    return done(null, profile);
  }
));

// Register investor
router.post('/register', async (req, res) => {
  try {
    const { email, password, company } = req.body;
    
    if (investors.has(email)) {
      return res.status(400).json({ error: 'Investor already registered' });
    }
    
    const hashedPassword = await bcrypt.hash(password, 10);
    const investorId = `inv_${Date.now()}`;
    
    investors.set(email, {
      id: investorId,
      email,
      password: hashedPassword,
      company,
      createdAt: new Date(),
      mfaEnabled: false,
      active: true
    });
    
    res.json({
      success: true,
      message: 'Investor registered successfully',
      investorId,
      nextStep: 'Enable MFA for security'
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Login
router.post('/login', async (req, res) => {
  try {
    const { email, password } = req.body;
    const investor = investors.get(email);
    
    if (!investor || !await bcrypt.compare(password, investor.password)) {
      return res.status(401).json({ error: 'Invalid credentials' });
    }
    
    if (!investor.active) {
      return res.status(403).json({ error: 'Account deactivated' });
    }
    
    // If MFA enabled, require verification
    if (investor.mfaEnabled) {
      const tempToken = jwt.sign(
        { email, mfaPending: true },
        JWT_SECRET,
        { expiresIn: '5m' }
      );
      return res.json({
        success: true,
        message: 'MFA required',
        tempToken,
        requireMFA: true
      });
    }
    
    // Issue JWT
    const token = jwt.sign(
      { id: investor.id, email },
      JWT_SECRET,
      { expiresIn: '24h' }
    );
    
    sessions.set(token, {
      investorId: investor.id,
      email,
      createdAt: new Date(),
      expiresAt: new Date(Date.now() + 24 * 60 * 60 * 1000)
    });
    
    res.json({
      success: true,
      token,
      investor: {
        id: investor.id,
        email: investor.email,
        company: investor.company
      }
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Setup MFA
router.post('/mfa/setup', (req, res) => {
  try {
    const { email } = req.body;
    const investor = investors.get(email);
    
    if (!investor) {
      return res.status(404).json({ error: 'Investor not found' });
    }
    
    const secret = speakeasy.generateSecret({
      name: `Bakhmach Hub Investor Portal (${email})`,
      issuer: 'Bakhmach Business Hub'
    });
    
    mfaSecrets.set(email, secret.base32);
    
    res.json({
      success: true,
      qrCode: secret.otpauth_url,
      secret: secret.base32,
      message: 'Scan QR code with authenticator app'
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Verify MFA code
router.post('/mfa/verify', (req, res) => {
  try {
    const { email, code } = req.body;
    const secret = mfaSecrets.get(email);
    
    if (!secret) {
      return res.status(400).json({ error: 'MFA not setup' });
    }
    
    const verified = speakeasy.totp.verify({
      secret,
      encoding: 'base32',
      token: code,
      window: 2
    });
    
    if (!verified) {
      return res.status(401).json({ error: 'Invalid MFA code' });
    }
    
    const investor = investors.get(email);
    investor.mfaEnabled = true;
    
    const token = jwt.sign(
      { id: investor.id, email },
      JWT_SECRET,
      { expiresIn: '24h' }
    );
    
    res.json({
      success: true,
      message: 'MFA enabled successfully',
      token
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Verify JWT token
router.get('/verify', (req, res) => {
  try {
    const token = req.headers.authorization?.split(' ')[1];
    
    if (!token) {
      return res.status(401).json({ error: 'No token provided' });
    }
    
    const decoded = jwt.verify(token, JWT_SECRET);
    const session = sessions.get(token);
    
    if (!session) {
      return res.status(401).json({ error: 'Session not found' });
    }
    
    res.json({
      valid: true,
      investor: decoded,
      expiresAt: session.expiresAt
    });
  } catch (error) {
    res.status(401).json({ valid: false, error: 'Invalid token' });
  }
});

// Logout
router.post('/logout', (req, res) => {
  try {
    const token = req.headers.authorization?.split(' ')[1];
    sessions.delete(token);
    
    res.json({ success: true, message: 'Logged out successfully' });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Google OAuth callback
router.get('/google/callback', passport.authenticate('google', { session: false }),
  (req, res) => {
    const token = jwt.sign(
      { id: req.user.id, email: req.user.emails[0].value },
      JWT_SECRET,
      { expiresIn: '24h' }
    );
    
    res.redirect(`/dashboard?token=${token}`);
  }
);

module.exports = router;

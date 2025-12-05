import express, { Request, Response } from 'express';
import cors from 'cors';
import helmet from 'helmet';

const app = express();
const PORT = process.env.PORT || 3001;
const API_VERSION = process.env.API_VERSION || 'v1';

app.use(helmet());
app.use(cors({
  origin: process.env.CORS_ORIGIN || '*',
  credentials: true
}));

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

app.use((req: Request, res: Response, next) => {
  const timestamp = new Date().toISOString();
  console.log(`[${timestamp}] ${req.method} ${req.path}`);
  next();
});

app.get('/health', (req: Request, res: Response) => {
  res.status(200).json({
    status: 'ok',
    message: 'Bakhmach Business Hub API is running',
    version: API_VERSION,
    timestamp: new Date().toISOString()
  });
});

app.get('/api/' + API_VERSION, (req: Request, res: Response) => {
  res.status(200).json({
    message: 'Bakhmach Business Hub API',
    version: API_VERSION,
    endpoints: {
      auth: '/api/' + API_VERSION + '/auth',
      pdps: '/api/' + API_VERSION + '/pdps',
      goals: '/api/' + API_VERSION + '/goals',
      tasks: '/api/' + API_VERSION + '/tasks',
      analytics: '/api/' + API_VERSION + '/analytics'
    }
  });
});

app.use((req: Request, res: Response) => {
  res.status(404).json({
    error: 'NOT_FOUND',
    message: `Route ${req.method} ${req.path} not found`,
    timestamp: new Date().toISOString()
  });
});

app.use((err: any, req: Request, res: Response) => {
  console.error('Error:', err);
  res.status(500).json({
    error: 'INTERNAL_SERVER_ERROR',
    message: err.message || 'Internal server error',
    timestamp: new Date().toISOString()
  });
});

app.listen(PORT, () => {
  const timestamp = new Date().toISOString();
  console.log(`[${timestamp}] Bakhmach Business Hub API listening on port ${PORT}`);
  console.log(`[${timestamp}] Health check: http://localhost:${PORT}/health`);
  console.log(`[${timestamp}] API Base: http://localhost:${PORT}/api/${API_VERSION}`);
});

export default app;

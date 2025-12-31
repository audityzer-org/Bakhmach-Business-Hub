# mwan3 Dual-WAN Failover Setup Guide
## Bakhmach Business Hub - Energy Monitoring System

### Quick Summary
- **Primary WAN**: eth0 (ISP - Kyivstar/Vodafone)
- **Backup LTE**: usb0 (USB modem with backup SIM)
- **Failover Time**: ~15 seconds
- **Load Balance**: 3:1 (primary:backup)
- **Critical Services**: Prometheus, SSH, NTP (prefer primary)

---

## 1. PREREQUISITES

### Hardware
- OpenWrt Router (TP-Link Archer C7, Netgear WNDR) OR Linux with iptables
- USB LTE Modem: Huawei E3372h, ZTE MF823, or Qualcomm-based
- Ethernet cable (primary WAN)
- Backup SIM card (Kyivstar/Vodafone)

### Software Packages
```bash
opkg update
opkg install mwan3 mwan3luci ip ipset iptables kmod-usb-core kmod-usb-net
opkg install usb_modeswitch ppp kmod-usb-net-huawei-cdc-ncm  # For Huawei
```

---

## 2. USB MODEM SETUP

### Step 2.1: Identify Modem Device
```bash
lsusb
# Expected output:
# Bus 001 Device 002: ID 12d1:1506 Huawei Technologies Co., Ltd. E3372h
```

### Step 2.2: Switch Modem to Network Mode
Create `/etc/usb-mode.conf`:
```ini
[Huawei_E3372]
TargetVendor=0x12d1
TargetProduct=0x1506
MessageEndpoint=0x01
MessageContent=55534243785a0001000000000000061e000000000000000000000000000000
```

Switch modem:
```bash
usb_modeswitch -c /etc/usb-mode.conf
sleep 5
ls /dev/ttyUSB* /dev/cdc-wdm*  # Should see /dev/ttyUSB0, /dev/cdc-wdm0
```

### Step 2.3: Configure PPP Connection

Edit `/etc/ppp/peers/huawei`:
```
/dev/cdc-wdm0 115200
crtscts
defaultroute
noauth
user internet
password internet
lock
connect '/usr/sbin/chat -v -f /etc/ppp/chat/huawei.chat'
```

Create `/etc/ppp/chat/huawei.chat`:
```
ABORT BUSY
ABORT NO CARRIER
ABORT VOICE
OK ATZ
OK-ATZ-OK ATD*99***1#
CONNECT \d\c
```

Start connection:
```bash
pppd call huawei
ifconfig ppp0  # Verify IP assigned
```

---

## 3. NETWORK INTERFACE CONFIGURATION

### Step 3.1: Configure eth0 (Primary WAN)

Edit `/etc/config/network`:
```
config interface 'Primary_WAN'
    option ifname 'eth0'
    option proto 'dhcp'
    option metric '10'
    option customdns '8.8.8.8 1.1.1.1'
```

Apply changes:
```bash
/etc/init.d/network restart
```

### Step 3.2: Configure usb0 (Backup LTE)

Add to `/etc/config/network`:
```
config interface 'Backup_LTE'
    option ifname 'usb0'
    option proto 'dhcp'
    option metric '20'
```

Or for PPP:
```
config interface 'Backup_LTE'
    option proto 'ppp'
    option device '/dev/cdc-wdm0'
```

---

## 4. COPY mwan3 CONFIGURATION

```bash
cd /etc/config/
wget https://raw.githubusercontent.com/romanchaa997/Bakhmach-Business-Hub/main/monitoring/mwan3.yml
mv mwan3.yml mwan3

# Verify
cat mwan3
```

---

## 5. ENABLE AND START mwan3

```bash
/etc/init.d/mwan3 enable
/etc/init.d/mwan3 start

# Check status
mwan3 status

# Expected output:
# Interface Primary_WAN status: ONLINE
# Interface Backup_LTE status: ONLINE
```

---

## 6. MONITOR & TROUBLESHOOT

### Check Real-Time Status
```bash
mwan3 status
mwan3 list

# Detailed tracking
watch -n 2 'mwan3 status'
```

### View Routing Tables
```bash
ip route show table 100  # Primary_WAN
ip route show table 200  # Backup_LTE
ip route show table 201  # mwan3 main table
```

### Test Failover Manually
```bash
# Simulate primary WAN down
ifdown Primary_WAN
mwan3 status  # Should show usb0 as ONLINE

# Bring primary back
ifup Primary_WAN
mwan3 status  # Should switch back
```

### Common Issues & Fixes

**Issue**: usb0 interface not appearing
```bash
# Fix: Reinitialize USB
usb_modeswitch -W -c /etc/usb-mode.conf
udevadm trigger
```

**Issue**: mwan3 fails to start
```bash
# Fix: Check logs
logread | grep mwan3
# Restart
/etc/init.d/mwan3 restart
```

**Issue**: Slow failover (>30 seconds)
```bash
# Edit /etc/config/mwan3, reduce:
# interval from 5s to 3s
# down from 3 to 2
# (Note: increases CPU usage)
```

---

## 7. PROMETHEUS & MONITORING

### Scrape mwan3 Status

Add to prometheus.yml:
```yaml
- job_name: 'mwan3'
  static_configs:
    - targets: ['localhost:9100']  # node_exporter for interface stats
  metric_relabel_configs:
    - source_labels: [__name__]
      regex: 'node_network.*'
      action: keep
```

### Alert Rules

`/etc/prometheus/rules/mwan3_alerts.yml`:
```yaml
groups:
  - name: mwan3
    rules:
      - alert: Primary_WAN_Down
        expr: mwan3_interface_status{interface="Primary_WAN"} == 0
        for: 30s
        annotations:
          summary: "Primary WAN interface down"
```

---

## 8. COST OPTIMIZATION FOR LTE

1. **High check interval**: 10 seconds (not 5) for Backup_LTE
2. **Compress Prometheus**: Use gzip before sending over LTE
3. **Disable updates on LTE**: Only fetch metrics on primary
4. **Data limits**: Set max 5 Mbps on usb0

```bash
# Limit bandwidth
tc qdisc add dev usb0 root tbf rate 5mbit burst 32kbit latency 400ms
```

---

## 9. PRODUCTION CHECKLIST

- [ ] eth0 working (ping 8.8.8.8)
- [ ] usb0 modem initialized
- [ ] Both interfaces have IPs
- [ ] mwan3 service starts without errors
- [ ] Default route uses eth0 first
- [ ] Failover test successful (ifdown eth0 → usb0 active)
- [ ] Prometheus scraping mwan3 metrics
- [ ] SSH always prefers primary (policy: Primary_Only)
- [ ] Alerts configured for WAN downtime
- [ ] Uptime >99.5% over 30 days

---

## References

- [OpenWrt mwan3 Docs](https://openwrt.org/docs/guide_user/services/vpn/mwan3)
- [Huawei E3372 Setup](https://openwrt.org/inbox/toh/huawei/huawei_e3372)
- [Prometheus Node Exporter](https://github.com/prometheus/node_exporter)

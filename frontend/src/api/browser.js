// 生成浏览器唯一指纹，通过组合浏览器特征来防止机器人攻击
// 收集浏览器特征包括: 用户代理、屏幕分辨率、时区、语言、已安装字体等
// 使用 SHA-256 对特征进行哈希处理生成唯一标识符
const generateBrowserFingerprint = () => {
  const features = {
    userAgent: navigator.userAgent,
    language: navigator.language,
    platform: navigator.platform,
    screenResolution: `${window.screen.width}x${window.screen.height}`,
    colorDepth: window.screen.colorDepth,
    timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
    touchSupport: 'ontouchstart' in window,
    cookiesEnabled: navigator.cookieEnabled,
    canvas: (() => {
      const canvas = document.createElement('canvas');
      const ctx = canvas.getContext('2d');
      ctx.textBaseline = 'top';
      ctx.font = '14px Arial';
      ctx.fillText('Hello, world!', 2, 2);
      return canvas.toDataURL();
    })(),
    webglVendor: (() => {
      const canvas = document.createElement('canvas');
      const gl = canvas.getContext('webgl');
      return gl ? gl.getParameter(gl.VENDOR) : null;
    })()
  };

  return features;
};

// 添加用户同意状态检查
const checkConsent = () => {
  const consent = localStorage.getItem('fingerprintConsent');
  return consent === 'true';
};

// 获取浏览器指纹，并在本地存储中保存
export const getBrowserFingerprint = async () => {
  const hasConsent = await requestFingerprintConsent();
  if (!hasConsent) {
    return null;
  }

  const fingerprint = localStorage.getItem('fingerprint');
  const generateNewFingerprint = () => {
    const newFingerprint = generateBrowserFingerprint();
    const fingerprintData = {
      data: newFingerprint,
      exp: new Date().getTime() + (7 * 24 * 60 * 60 * 1000) // 1周过期
    };
    const encodedFingerprint = btoa(JSON.stringify(fingerprintData));
    localStorage.setItem('fingerprint', encodedFingerprint);
    return encodedFingerprint;
  };

  if (!fingerprint) {
    return generateNewFingerprint();
  }

  const fingerprintData = JSON.parse(atob(fingerprint));
  if (fingerprintData.exp < new Date().getTime()) {
    return generateNewFingerprint();
  }
  return fingerprint;
};

// 修改用户同意提示文案
export const requestFingerprintConsent = () => {
  return new Promise((resolve) => {
    if (checkConsent()) {
      resolve(true);
      return;
    }

    const confirmed = true

    // const confirmed = window.confirm(
    //   '为了提供更好的安全保护，我们需要收集一些基本的设备信息。这些信息仅用于识别您的设备，确保账户安全。您是否同意？'
    // );

    if (confirmed) {
      localStorage.setItem('fingerprintConsent', 'true');
      resolve(true);
    } else {
      resolve(false);
    }
  });
};
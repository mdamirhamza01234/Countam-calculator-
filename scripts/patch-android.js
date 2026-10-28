// CI helper: `npx cap add android` ke baad generated android/ project ko patch karta hai
// (fixed signing key, camera permission, google-services.json). Kuch na mile to build fail ho jaata hai.
const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
const appDir = path.join(root, 'android', 'app');

// 1) Signing config (stable SHA-1 => Firebase Google login har build mein chalega)
const gradlePath = path.join(appDir, 'build.gradle');
let gradle = fs.readFileSync(gradlePath, 'utf8');
if (!gradle.includes('signingConfigs')) {
  const signing = `
    signingConfigs {
        release {
            storeFile file(System.getenv("KS_PATH") ?: "../../android-signing/mittu.keystore")
            storePassword System.getenv("KS_PASS") ?: "mittu123456"
            keyAlias System.getenv("KS_ALIAS") ?: "mittu"
            keyPassword System.getenv("KS_KEY_PASS") ?: "mittu123456"
        }
    }
    buildTypes {`;
  if (!/\n\s*buildTypes\s*\{/.test(gradle)) throw new Error('buildTypes block nahi mila in app/build.gradle');
  gradle = gradle.replace(/\n\s*buildTypes\s*\{/, signing);
  if (!/release\s*\{/.test(gradle)) throw new Error('release block nahi mila');
  gradle = gradle.replace(/(buildTypes\s*\{\s*release\s*\{)/, '$1\n            signingConfig signingConfigs.release');
  fs.writeFileSync(gradlePath, gradle);
}

// 2) Manifest permissions (file chooser mein Camera option ke liye)
const manifestPath = path.join(appDir, 'src', 'main', 'AndroidManifest.xml');
let manifest = fs.readFileSync(manifestPath, 'utf8');
['android.permission.CAMERA', 'android.permission.READ_MEDIA_IMAGES'].forEach(p => {
  if (!manifest.includes(p)) manifest = manifest.replace('</manifest>', `    <uses-permission android:name="${p}" />\n</manifest>`);
});
fs.writeFileSync(manifestPath, manifest);

// 3) Firebase google-services.json (repo root mein rakhein)
const gs = path.join(root, 'google-services.json');
if (fs.existsSync(gs)) {
  fs.copyFileSync(gs, path.join(appDir, 'google-services.json'));
  console.log('google-services.json copy ho gayi');
} else {
  console.warn('WARNING: google-services.json repo root mein nahi mili — Google login APK mein kaam nahi karega.');
}
// 4) Android 12+ system splash: black background (white flash nahi)
try {
  const stylesPath = path.join(appDir, 'src', 'main', 'res', 'values', 'styles.xml');
  let styles = fs.readFileSync(stylesPath, 'utf8');
  if (!styles.includes('windowSplashScreenBackground')) {
    styles = styles.replace(/(<style name="AppTheme.NoActionBarLaunch"[^>]*>)/, '$1\n        <item name="android:windowSplashScreenBackground">#000000</item>');
    fs.writeFileSync(stylesPath, styles);
  }
} catch (e) { console.warn('styles.xml patch skip:', e.message); }
console.log('Android project patch ho gaya');

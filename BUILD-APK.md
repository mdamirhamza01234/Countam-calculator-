# Mittu Wholesaler APK (GitHub se build)

APK GitHub Actions se banta hai (Capacitor). App `https://kiranabillgenerator.vercel.app` ko kholta hai,
isliye website update hote hi app mein bhi update aa jaata hai — har baar naya APK nahi chahiye.

## APK kaise banayein
1. GitHub repo → **Actions** → **Build Android APK** → **Run workflow**.
2. 5-8 minute baad **Releases → "Mittu Wholesaler APK (latest)"** se `Mittu-Wholesaler.apk` phone mein download karke install karein.

## Google login ke liye (ek baar)
1. Firebase Console → project `mittu-billing` → Project settings → **Add app → Android**.
   - Package name: `com.mittu.billing`
   - SHA-1: `CA:71:53:35:A9:73:95:8C:A9:43:B2:9C:85:94:F4:42:04:E4:0A:7D`
2. `google-services.json` download karke repo ke **root** mein upload karein (same level par `package.json`).
3. Authentication → Sign-in method → Google enabled hona chahiye.
4. Actions se APK dobara build karein.

## Icon (optional)
`resources/icon.png` (1024x1024) upload karein — build mein apne aap icon ban jayega.

## Dhyan
- `android-signing/mittu.keystore` APK ko hamesha ek hi signature deta hai (SHA-1 nahi badalta). Repo public hai, isliye
  baad mein is keystore ko GitHub Secrets mein shift karna behtar hai.
- `android/` folder CI mein har baar naya banta hai, repo mein nahi hai.

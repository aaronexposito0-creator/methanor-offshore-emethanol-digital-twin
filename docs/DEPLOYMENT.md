# Deployment

MethaNor is a static site: there is no server-side runtime and no secrets.

## GitHub Pages

1. Push the repository to GitHub.
2. Open **Settings → Pages**.
3. Under *Build and deployment*, select **Deploy from a branch**.
4. Branch: `main`, folder: `/ (root)`.
5. Save.

The app will be available at the Pages URL after deployment.

## Local

```bash
python -m http.server 8000
```

Open `http://localhost:8000`.

## Netlify / Vercel

Import the repository as a static project. No build command is required; publish the repository root.

## Render Static Site

Use **New → Static Site** (not Web Service), connect the GitHub repository and publish the repository root. No build command or Python start command is required. This avoids unnecessary server sleep/startup behaviour for a fully static application.

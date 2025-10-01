# Source Assets

This folder is for assets that need to be imported and processed by the build system.

## Usage

For assets that need to be imported in components:

```tsx
import logoImage from '../assets/logo.png';

// Then use in component
<img src={logoImage} alt="Logo" />
```

## Asset Types

- Images that need optimization
- Icons and graphics
- Fonts
- Other static resources

## Build Processing

Assets in this folder will be:
- Processed by Vite
- Optimized for production
- Given hashed filenames for caching
- Bundled with the application

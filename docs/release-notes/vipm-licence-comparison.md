# VIPM License Comparison

VI Package Manager (VIPM) is available in multiple editions to serve different needs within the LabVIEW development community. This guide compares the features and capabilities of each edition to help you select the most appropriate version for your requirements.

## Available Editions

The three primary VIPM editions are:

- **VIPM Community**: Advanced features typically reserved for Pro, but restricted to non-commercial use only
- **VIPM Free**: Basic version that is free for commercial use
- **VIPM Pro**: The full-featured commercial version for professional development

## Legend

- ✅ Fully included
- ☑️ Partially included
- ❌ Not included

## Features and Functionality Comparison

| Feature | Community | Free | Pro |
|---------|-----------|------|-----|
| **Commercial Use** | ❌ | ✅ | ✅ |
| **Included with LabVIEW** (*Requires online activation) | ❌* | ✅ | ❌* |

### Build Automation

| Feature | Community | Free | Pro |
|---------|-----------|------|-----|
| **VIPM API for LabVIEW** | ✅ | ✅ | ✅ |
| **New Command-line Interface (CLI)** (2026+) | ☑️ | ☑️ | ✅ |

### Package Installing

| Feature | Community | Free | Pro |
|---------|-----------|------|-----|
| **Install addon** | ✅ | ✅ | ✅ |
| **Multiple LV version & target** (64 vs 32 bit) | ✅ | ✅ | ✅ |
| **Create VIPC for dependency management** | ✅ | ✅ | ✅ |
| **Store packages inside VIPC file for offline installation** | ✅ | ❌ | ✅ |
| **Apply VIPC** | ✅ | ✅ | ✅ |
| **Per Project Install** (in development ~2027+) | ✅ | ❌ | ✅ |

### Package Building

| Feature | Community | Free | Pro |
|---------|-----------|------|-----|
| **Build reuse library packages** | ✅ | ✅ | ✅ |
| **Build reuse system packages** | ✅ | ✅ | ✅ |
| **Build LabVIEW developer extension packages** | ✅ | ✅ | ✅ |
| **Customizable function and control palettes** | ✅ | ✅ | ✅ |
| **Link to external dependencies** | ✅ | ✅ | ✅ |
| **3rd party licensing and activation** | ❌ | ❌ | ✅ |
| **VI password protection** | ✅ | ❌ | ✅ |

### Package Publishing

| Feature | Community | Free | Pro |
|---------|-----------|------|-----|
| **Create and manage repos** | ❌ | ❌ | ✅ |
| **Publish addons on private internal repo** | ❌ | ❌ | ✅ |

### Package Finding

| Feature | Community | Free | Pro |
|---------|-----------|------|-----|
| **Subscribe to additional ("custom") repo** | ✅ | ❌ | ✅ |
| **Subscribed to "NI Tool Network" and "VIPM Community" repo** | ✅ | ✅ | ✅ |

### Project Dependency Management (DRAGON)

| Feature | Community | Free | Pro |
|---------|-----------|------|-----|
| **Dependencies on NI drivers/nipkg** (in development) | ✅ | ✅ | ✅ |
| **.dragon file project package dependencies** | ✅ | ✅ | ✅ |
| **Dragon Project GUI** | ✅ | ✅ | ✅ |

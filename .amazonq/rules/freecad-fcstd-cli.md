# FreeCAD .FCStd File CLI Manipulation

## File Format Overview

FreeCAD `.FCStd` files are ZIP archives containing:
- `Document.xml` - Main document structure and properties
- `GuiDocument.xml` - GUI-specific settings
- Various data files for objects and features

## CLI Operations

### Viewing Contents

```bash
# List all files in .FCStd archive
unzip -l file.FCStd

# View Document.xml content
unzip -p file.FCStd Document.xml
```

### Search and Replace in Document.xml

#### Basic Pattern Replacement
```bash
# Extract, modify, update archive
unzip -p file.FCStd Document.xml | sed 's/old_pattern/new_pattern/g' > /tmp/Document.xml
zip -u file.FCStd /tmp/Document.xml
rm /tmp/Document.xml
```

#### One-liner Function
```bash
fcstd_sed() {
    unzip -p "$1" Document.xml | sed "s/$2/$3/g" > /tmp/Document.xml && zip -u "$1" /tmp/Document.xml && rm /tmp/Document.xml
}

# Usage
fcstd_sed model.FCStd "OldName" "NewName"
```

### Common Use Cases

#### Rename Objects
```bash
fcstd_sed model.FCStd 'name="Part"' 'name="NewPart"'
```

#### Update Properties
```bash
fcstd_sed model.FCStd 'radius="[0-9.]*"' 'radius="25.0"'
```

#### Change Labels
```bash
fcstd_sed model.FCStd 'label="OldLabel"' 'label="NewLabel"'
```

## Key Commands

- `unzip -p` - Extract file to stdout (no disk files created)
- `zip -u` - Update existing files in archive
- `sed 's/pattern/replacement/g'` - Global search and replace

## Notes

- Always backup `.FCStd` files before modification
- Changes affect the internal document structure
- FreeCAD must reload files to see changes
- Use proper XML escaping for special characters

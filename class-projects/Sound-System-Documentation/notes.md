# Notes and Change Log

Use this file to record configuration changes, troubleshooting steps, and operational notes.

## System Diagram Types

- **System diagram** - Overall system architecture
- **Signal flow diagram/single line diagram** - Simplified signal paths

*Break line at the bottom means this block shows up more than once but it is the same thing*

## DXF Data Extraction Results (Feb 13, 2026)

Successfully extracted data from AutoCAD DXF files using Python + ezdxf library.

**Files Created:**
- `extract_dxf.py` - Basic extraction script
- `extract_dxf_enhanced.py` - Enhanced with layer organization
- `*_by_layer.json` - All data organized by layer
- `*_equipment_list.json` - Structured equipment list
- `*_layer_report.txt` - Comprehensive text report

**Data Found:**
- 325 equipment entries total
- 31 layers (AV-EQUIP, AV-CONNECT, AV-TXTLT, etc.)
- 446 text elements
- 36 loudspeaker symbols
- 642 connection lines
- 30 circles, 126 polylines

**Key Findings:**
- Equipment organized by layer type (equipment, text, connections)
- Labels on AV-TXTLT and 0-text layers
- Connection lines on AV-CONNECT layer
- Equipment geometry on AV-EQUIP layer
- 16 wireless lavalier mics for cast members
- 2 system processors for different zones
- Mix system uses ACE network protocol

**Visualization Approach:**
- **Mermaid** - Good for documentation, version control friendly, lives in markdown
- **Draw.io** - Better for presentation, full visual control, requires extension
- Both created from extracted DXF data

## Layer Organization Strategy

Organizing by layers helps identify:
1. Equipment vs. labels vs. connections
2. Signal types (audio, control, 70V, etc.)
3. Related components grouped by function
4. Positioning and spatial relationships

This allows for more accurate and complete diagram generation.
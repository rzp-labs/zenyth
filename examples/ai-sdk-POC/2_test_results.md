# Claude Code Performance Test Results

## Executive Summary
- **Root Cause Identified**: 55+ second delays caused by CLAUDE.md mandatory initialization, not MCP loading
- **Performance Improvement**: 20x speedup achieved (55s → 2.8s) by optimizing CLAUDE.md
- **Key Finding**: Permission timeouts, not computational overhead, drive most delays
- **MCP Tools Performance**: Rich tooling adds minimal overhead (~0.25s for 26 additional tools)
- **Modular vs Monolithic**: 0.5s overhead for modular CLAUDE.md provides superior maintainability
- **Context Loading**: Large context (50K+ tokens) is viable with fixed-cost Claude Code subscription

## Test Results

### 1. Baseline Performance Tests

#### Direct CLI (No Flags)
```bash
claude --print --output-format json "What is 2+2?"
```
- **Result**: 2.73s total, 2.21s duration_ms, 3.47s duration_api_ms
- **Status**: ✅ Baseline performance

#### AI SDK Wrapper (Initial)
```bash
curl -X POST http://localhost:3001/v1/chat/completions
```
- **Result**: 55.97s total
- **Status**: ❌ 24x slower than direct CLI

### 2. Configuration Impact Analysis

| Configuration | Time | Delta | Notes |
|---------------|------|-------|-------|
| Direct CLI | 2.73s | baseline | Optimal |
| + model flag | 2.25s | -0.48s | Slightly faster |
| + add-dir | 4.75s | +2.02s | Moderate overhead |
| + mcp-config | 57.86s | +55.13s | ❌ Major bottleneck |

### 3. Output Format Comparison

| Format | Time | Overhead | Use Case |
|--------|------|----------|----------|
| JSON | 2.73s | baseline | Fastest |
| Stream-JSON | 3.77s | +1.04s | Real-time feedback |
| Text | 6.51s | +3.78s | ❌ Slowest |

**Key Insight**: JSON format is fastest, contradicting initial assumptions.

### 4. Model Performance Analysis

| Model | Time | Status | Speed Ranking |
|-------|------|--------|---------------|
| Haiku (claude-3-5-haiku-20241022) | 3.65s | ✅ Success | Fastest |
| Sonnet (default) | 3.41s | ✅ Success | Medium |
| Opus | 13.59s | ❌ Error | Slowest |

### 5. Permission vs Performance Trade-off

| Configuration | Time | Security Level |
|---------------|------|----------------|
| Default permissions | 2.90s | High ✅ |
| Skip permissions | 2.49s | None ❌ |
| **Delta** | **0.41s** | **Trade-off not worth risk** |

**Recommendation**: Keep default permissions (only 0.41s overhead).

### 6. CLAUDE.md Impact Discovery

#### Complex CLAUDE.md (Original)
```bash
claude --print --mcp-config .mcp.json "What is 3+3?"
```
- **Result**: 57.86s total
- **Behavior**: Full initialization sequence with tool calls
- **Output**: `[SESSION INITIALIZED]` with mode declarations

#### No CLAUDE.md
```bash
# With CLAUDE.md moved away
claude --print --mcp-config .mcp.json "What is 10+10?"
```
- **Result**: 55+ seconds (timeout)
- **Behavior**: Waiting for directory trust approval
- **Issue**: Permission prompt in non-interactive mode

#### Fast CLAUDE.md (Optimized)
```bash
claude --print --mcp-config .mcp.json "What is 12+12?"
```
- **Result**: 2.81s total
- **Improvement**: 20x speedup (57.86s → 2.81s)
- **Key**: Removed mandatory tool execution requirements

### 7. Streaming Performance with Optimized Config

| Output Format | Time | API Time | Notes |
|---------------|------|----------|-------|
| JSON | 2.59s | 3.03s | Fastest overall |
| Stream-JSON + verbose | 2.67s | 5.94s | +0.08s for streaming |
| Text | 2.81s | N/A | Slightly slower |

**Stream-JSON Verdict**: 0.08s overhead worth it for real-time feedback and monitoring.

### 8. Large Context Loading Tests

#### Monolithic CLAUDE.md (3,027 lines)
```bash
claude --print --output-format stream-json --verbose --mcp-config .mcp.test.json "What is 18+18?"
```
- **Result**: 7.58s total, 10.05s API time
- **Token count**: 50,598 tokens
- **MCP servers**: 5/6 connected (26 additional tools)
- **Tools available**: 36 total (10 basic + 26 MCP)

#### Large Context Impact Analysis
| Context Size | Time | Token Count | Tools | Use Case |
|--------------|------|-------------|-------|-----------|
| **Minimal** | 2.67s | 1,040 | 10 basic | Simple queries |
| **Large context only** | 7.33s | 41,708 | 10 basic | Rich knowledge |
| **Large + MCP tools** | 7.58s | 50,598 | 36 enhanced | Full capabilities |

**Key Insight**: MCP tool loading adds only 0.25s overhead for 26 additional specialized tools.

### 9. Modular vs Monolithic CLAUDE.md

#### Complete Line Count Verification
- **Monolithic CLAUDE.md**: 3,027 lines (single file)
- **Modular structure**: 3,063 lines total (9 organized files)
- **Content preservation**: ✅ Complete with proper @import structure

#### Performance Comparison
| Approach | Time | Token Count | Maintainability | File Count |
|----------|------|-------------|----------------|------------|
| **Monolithic** | 6.64s | 50,686 | ❌ Poor | 1 large file |
| **Modular** | 7.20s | 51,208 | ✅ Excellent | 9 organized files |
| **Delta** | **+0.56s** | +522 tokens | Major improvement | 8x more organized |

**Key Finding**: 0.56s overhead (8%) for dramatically better organization and team collaboration.

#### Modular File Structure
```
CLAUDE.md (47 lines - @import statements)
├── @docs/agent/rules.md (66 lines)
├── @docs/development/commands.md (51 lines)
├── @docs/architecture/overview.md (31 lines)
├── @docs/architecture/zenyth_overview.md (274 lines)
├── @docs/architecture/solid_principles.md (393 lines)
├── @docs/development/semantic_clarity.md (271 lines)
├── @docs/development/challenging_rules.md (388 lines)
├── @docs/testing/strategy.md (21 lines)
└── @docs/architecture/implementation_plan.md (1,527 lines)
```

## Critical Findings

### 1. Performance Bottleneck Hierarchy
1. **CLAUDE.md mandatory initialization**: 55s penalty
2. **Permission timeout waits**: 50+ seconds in non-interactive mode  
3. **MCP config flag**: Triggers above issues (+0.3s inherent overhead)
4. **Add-dir flag**: +2s overhead
5. **Modular file structure**: +0.56s overhead (excellent maintainability trade-off)
6. **Output format choice**: 0.08s-3.78s range
7. **Permission skip**: -0.41s gain (not worth security risk)

### 2. AI SDK Wrapper Root Cause
The wrapper's 55s delay was caused by:
```javascript
'--mcp-config', path.join(__dirname, '.mcp.json')
```
This flag triggered CLAUDE.md initialization, not the AI SDK itself.

### 3. Fast CLAUDE.md Design Principles
❌ **Avoid**: Mandatory requirements (`**MUST**`, `**[CRITICAL]**`)
❌ **Avoid**: Forced tool execution checklists
❌ **Avoid**: Session initialization requirements
✅ **Include**: Documentation and guidance
✅ **Include**: Command examples and workflows
✅ **Include**: Project context and architecture

## Performance Recommendations

### For Production API Wrapper
1. **Use modular CLAUDE.md structure**: Superior maintainability for 0.56s cost
2. **Load MCP tools by default**: 26 additional tools for only 0.25s overhead
3. **Keep default permissions**: Security worth 0.41s
4. **Use stream-JSON**: 0.08s overhead worth monitoring capabilities
5. **Embrace rich context**: No token costs with Claude Code subscription

### Context Loading Strategy (Updated)
```javascript
// Default to rich capabilities - no token costs!
const defaultConfig = {
  claudeMd: 'modular',        // 7.2s, excellent maintainability
  mcpTools: 'comprehensive',  // 36 tools, extensive capabilities
  outputFormat: 'stream-json' // Real-time monitoring
};

// Only optimize for speed when absolutely critical
const speedOptimized = {
  claudeMd: 'minimal',        // 2.7s, basic functionality
  mcpTools: 'none',          // 10 basic tools only
  outputFormat: 'json'       // Fastest output
};
```

### For High-Performance Scenarios
```bash
# Optimal comprehensive command (RECOMMENDED)
claude --print --output-format stream-json --verbose --mcp-config .mcp.comprehensive.json "prompt"  
# Expected: ~7.2s, 36 tools, real-time monitoring

# Optimal speed command (when latency critical)
claude --print --output-format json --model claude-3-5-haiku-20241022 "prompt"
# Expected: ~2.3s, basic tools
```
# AI Scene Generator – Full Experiment Log

## Objective

Build a system that:

* Generates story scenes using an LLM
* Converts scenes into images (Stable Diffusion)
* Maintains **character consistency across scenes**
* Generates narration audio

---

# Phase 1: Initial Setup

### Approach

* Used OpenAI (`gpt-4o-mini`) for scene generation
* Used Stable Diffusion v1.5 locally
* Generated images independently per scene

### Problems

1. ❌ No character consistency
2. ❌ Each image had a completely different robot
3. ❌ Prompt engineering alone failed

### Insight

> Stable Diffusion alone cannot maintain character identity across generations

---

# Phase 2: Prompt Engineering Attempts

### Changes Tried

* Added detailed prompts:

  * "same robot"
  * "consistent character"
  * "yellow robot"

### Problems

1. ❌ Still different robots
2. ❌ Model ignored identity instructions
3. ❌ Overfitting to generic robot concepts

### Insight

> Prompt ≠ identity control

---

# Phase 3: Img2Img Introduction

### Hypothesis

Use previous image as input to enforce consistency

### Implementation

* Switched to `StableDiffusionImg2ImgPipeline`
* Passed previous image as `init_image`

### Problems

1. ❌ First image became nearly white (blank canvas issue)
2. ❌ Noise propagation across scenes
3. ❌ Character drift still present

### Insight

> Img2Img is NOT designed for identity consistency

---

# Phase 4: Negative Prompt Tuning

### Negative Prompt Used

* "multiple robots"
* "extra limbs"
* "mutated"

### Problems

1. ❌ Did not fix identity
2. ❌ Only removed artifacts

### Insight

> Negative prompts = artifact control, not identity control

---

# Phase 5: NSFW Issues

### Observed

* Black images generated
* NSFW filter triggered

### Root Cause

* Words like "child" in LLM output

### Fix

* Updated prompt:

  * "Only robots, no humans, no children"

---

# Phase 6: LLM Issues

### Problems

1. ❌ LLM returned inconsistent schema
2. ❌ Missing fields (`image_prompt`, `description`)
3. ❌ JSON parsing failures

### Fixes

* Regex extraction for JSON
* Schema enforcement in prompt
* Fallback logic in code

---

# Phase 7: Git Setup Issues

### Problems

* Remote conflicts
* Non-fast-forward errors
* Merge conflicts in `.gitignore`

### Fixes

* Used `--allow-unrelated-histories`
* Resolved merge conflicts manually
* Set upstream branch

---

# Phase 8: Move to Local LLM (Ollama)

### Reason

* Reduce cost
* Avoid API dependency

### Implementation

* Used `llama3` via Ollama

### Problems

1. ❌ Output formatting inconsistent
2. ❌ Returned markdown + text

### Fix

* Strict JSON prompt
* Regex extraction

---

# Phase 9: ControlNet Exploration (Conceptual)

### Discussion

* Needed structure control
* Not implemented yet

---

# Phase 10: IP-Adapter Introduction

### Goal

Maintain character identity

### Setup

* Loaded `h94/IP-Adapter`
* Used reference image

### Problems

1. ❌ Version mismatch errors

   * `slice_size` missing
2. ❌ huggingface_hub import error

### Fixes

* Downgraded `huggingface_hub`
* Adjusted diffusers version

---

# Phase 11: Path Errors

### Error

```
ValueError: Incorrect path or URL
```

### Cause

* Wrong asset path

### Fix

* Ensured `assets/robot.png` exists

---

# Phase 12: JSON Schema Mismatch

### Problems

* Missing `image_prompt`
* Missing `description`

### Fix

* Derived prompt from fields:

  ```python
  image_prompt = f"{env}, {action}, {emotion}"
  ```

---

# Phase 13: Emotion Null Issue

### Problem

```
AttributeError: 'NoneType' object has no attribute 'lower'
```

### Cause

* LLM returned `"emotion": null`

### Fix

```python
emotion_text = (emotion or "neutral").lower()
```

---

# Phase 14: IP-Adapter Tuning Attempts

## Attempt 1: High Strength

* Result: identical images

## Attempt 2: Low Strength (0.3)

* Result: different robots

## Attempt 3: Medium Strength (0.6)

* Result: partial consistency

## Attempt 4: 0.75

* Result: better identity, still drift

## Attempt 5: 0.85

* Result: stronger identity, less variation

---

# Phase 15: Prompt Refinement

### Tried:

* Generic prompts → failed
* Detailed identity prompts → improved

### Best version:

```
same robot as reference image,
yellow and white humanoid robot,
blue circular eyes,
do not change design
```

---

# Phase 16: Generator Issue

### Problem

* Same seed → same pose

### Fix

```python
generator = torch.Generator().manual_seed(42 + idx)
```

---

# Phase 17: Final Observations

### What works

* Stable pipeline
* Good image quality
* Partial identity consistency

### What doesn't

* Exact character lock
* Structural consistency

---

# Final Insight

## 🔥 Core Learning

> Stable Diffusion + IP-Adapter = style consistency
> NOT = perfect character consistency

---

# Next Steps (Recommended)

## 1. ControlNet (Pose/Depth)

* Adds structure control

## 2. SDXL + IP-Adapter

* Better identity preservation

## 3. Combine both

* Production-grade pipeline

---

# Personal Learning Summary

You explored:

* Prompt engineering
* Diffusion models
* Img2Img
* Negative prompting
* NSFW filters
* LLM integration
* JSON parsing
* Git workflows
* IP-Adapter

---

# Conclusion

You have successfully moved from:
❌ Random generation
→
✅ Controlled generation pipeline

Next step is:
👉 Full control (identity + structure)

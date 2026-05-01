# AI Video Generation Project — Learning Log and System Documentation

---

## 1. Objective

The goal of this project is to build a fully local AI-driven system capable of generating videos from text prompts using a MacBook.

Target pipeline:

Prompt → Story → Scene Breakdown → Images → Consistent Character → Audio → Video → YouTube

Key constraints:

* No dependency on external APIs (e.g., OpenAI)
* Entire system runs locally
* Output quality should be suitable for publishing and eventual monetization

---

## 2. Current Status

At this stage, a working end-to-end pipeline has been implemented.

### Functional Components

* Text generation (LLM) for scene creation
* Image generation using Stable Diffusion (SD 1.5)
* Audio generation for narration
* Orchestration through a Python pipeline

### Integrated Techniques

* Prompt engineering for structured outputs
* Img2Img concepts
* IP-Adapter for visual conditioning
* ControlNet for structural guidance

### Engineering Progress

* Reliable execution across multiple runs
* Handling of model loading and local inference
* Integration of multiple components into a single workflow

---

## 3. Key Learnings

### 3.1 LLM Behavior

The language model is inherently non-deterministic. Common issues observed:

* Invalid JSON outputs
* Missing or inconsistent fields
* Occasional deviation from instructed format

Mitigation strategies:

* Regex-based JSON extraction
* Post-processing validation
* Fallback logic for missing fields

---

### 3.2 Stable Diffusion Fundamentals

A critical realization:

Stable Diffusion does not maintain memory of previously generated characters. Each generation is independent.

This explains:

* Variation in character appearance across scenes
* Lack of identity consistency

---

### 3.3 Img2Img

Img2Img is not a separate model but a variant of the same diffusion process with an initial image.

It improves continuity but does not solve identity consistency.

---

### 3.4 Initial Image Behavior

Using a blank (white) image as input results in weak guidance, often producing washed-out or low-detail outputs.

---

### 3.5 NSFW Filtering

Certain prompts triggered the model’s safety mechanisms, resulting in black images.

Triggers included:

* Ambiguous references to humans or children

Mitigation:

* Restrict prompts to robots and objects only

---

### 3.6 IP-Adapter

IP-Adapter introduces a reference image into the generation process.

Observed effects:

* Improved color consistency
* Partial stylistic alignment

Limitations:

* Does not enforce exact identity
* Cannot preserve structure reliably

---

### 3.7 ControlNet

ControlNet provides structural guidance.

Observed effects:

* Improved pose stability
* Better spatial consistency

Limitations:

* Does not maintain character identity
* Works independently of appearance consistency

---

### 3.8 Core Insight

There is a fundamental distinction between conditioning and learning.

Current approach:

* Prompt + IP-Adapter + ControlNet = conditioning

Required approach:

* Model fine-tuning (LoRA) = learning

---

## 4. Problems Encountered

### 4.1 LLM Issues

* Invalid JSON format
* Missing required fields
* Inconsistent schema across runs

---

### 4.2 Diffusion Issues

* Character inconsistency across scenes
* Low-detail or washed-out outputs
* Multiple unintended characters
* Visual artifacts

---

### 4.3 Integration Issues

* Dependency conflicts (e.g., huggingface_hub)
* Model download confusion
* File path issues (assets not found)
* Device warnings (CUDA vs MPS)

---

### 4.4 Runtime Errors

* JSON parsing failures
* KeyError due to missing fields
* NoneType errors during string operations

---

## 5. Fixes Implemented

### 5.1 LLM Handling

* Strict prompt formatting
* Regex-based JSON extraction
* Default scene fallback logic

---

### 5.2 Code Robustness

* Use of `.get()` instead of direct key access
* Null-safe handling
* Default values for missing fields

---

### 5.3 Image Generation Improvements

* Refined prompts
* Negative prompts to reduce artifacts
* Integration of IP-Adapter
* Integration of ControlNet

---

### 5.4 Stability Enhancements

* Fixed random seeds
* Controlled inference steps
* Enabled memory optimizations (attention slicing, VAE slicing)

---

## 6. Current Output Evaluation

| Aspect                | Status       |
| --------------------- | ------------ |
| Pipeline stability    | Stable       |
| Execution reliability | Consistent   |
| Image quality         | Moderate     |
| Character consistency | Poor         |
| Production readiness  | Not achieved |

---

## 7. Identified Limitation

Stable Diffusion 1.5 is the primary bottleneck.

Even with IP-Adapter and ControlNet:

* Identity is not preserved
* Character varies across scenes

Further tuning within SD 1.5 is unlikely to resolve this.

---

## 8. Conceptual Understanding

Current system behavior:

Conditioning-based generation:

* Each image is generated independently
* The model attempts to approximate the desired character

Required system behavior:

Learning-based generation:

* The model internalizes the character
* Outputs become consistent across scenes

---

## 9. Next Phase

The next step is to transition to a more capable setup:

SDXL + LoRA

### SDXL Advantages

* Improved realism
* Better composition
* Stronger prompt understanding

### LoRA Purpose

* Fine-tune the model on a specific character
* Enable consistent identity across generations

---

## 10. Roadmap

### Phase 1 (Completed)

* Basic pipeline construction
* Image generation setup
* Prompt control and debugging

---

### Phase 2 (Next)

* SDXL setup on local machine
* Dataset creation for the robot character
* LoRA training

---

### Phase 3

* Improved scene control using ControlNet
* Composition refinement

---

### Phase 4

* Frame sequencing
* Video generation pipeline

---

### Phase 5

* Audio integration (voice and music)
* Video editing and assembly
* YouTube publishing workflow

---

## 11. Strategic Direction

Further effort should not be spent on refining SD 1.5 outputs.

Focus should shift toward:

* Identity-aware generation
* Model fine-tuning
* Pipeline evolution

---

## 12. Summary

The current system is a functioning multi-component generative pipeline.

However, it is still in the conditioning stage and lacks character consistency.

The transition to SDXL and LoRA marks the shift from experimentation to controlled generation.

---

## 13. Next Action

Proceed with SDXL setup and begin preparation for LoRA training.

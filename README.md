3D_Scene_Interalization

# 3D Scene Internalization

**Goal:** Pretrain **scene-specific latent representations** to avoid expensive online 3D reconstruction, while supporting **override conditioning** (e.g., blocked doorway, new room, moved objects) at inference.  
This hybrid paradigm — **internalized base memory + contextual overrides** — enables **fast navigation, planning, and reasoning** in known environments with the flexibility to handle local changes.

---

## Motivation

For many navigation, planning, and reasoning tasks, agents repeatedly re-embed and reconstruct the 3D world from scratch, which is computationally expensive.  
Instead, this project explores **parametric models that internalize a fixed set of target scenes**, enabling:

- **Fast path planning** in known layouts.
- **Scene override reasoning** to adapt to local changes without retraining.
- **Exploration & map updates** with efficient reuse of pretrained memory.
- **Multi-step reasoning** in tasks requiring persistent spatial memory.
- **Design & simulation** for evaluating alternative scene layouts.

---

## Datasets

- **[Ego-Exo4D](https://ego-exo4d-data.org/)**  
  Multi-view dataset with ego + exo video, calibrated cameras, synchronized point clouds, gaze, and IMU.  
  🔒 Access requires permission request.

- **[HD-EPIC](https://hd-epic.github.io/)**  
  Large-scale **kitchen-based action dataset** with egocentric videos, fine-grained annotations, gaze, SLAM point clouds, and digital-twin reconstructions.  
  📦 Publicly downloadable (videos, annotations, SLAM outputs, VRS streams).

---

## Related Work (Anchor Papers)

- **[3D-Mem (CVPR 2025)](https://openaccess.thecvf.com/content/CVPR2025/papers/Yang_3D-Mem_3D_Scene_Memory_for_Embodied_Exploration_and_Reasoning_CVPR_2025_paper.pdf)** – persistent 3D scene memory for embodied exploration.
- **[Agent3D-Zero (ECCV 2024)](https://www.ecva.net/papers/eccv_2024/papers_ECCV/papers/02877.pdf)** – zero-shot 3D understanding with active viewpoint selection.
- **[3D-LLM (NeurIPS 2023)](https://proceedings.neurips.cc/paper_files/paper/2023/file/413885e70482b95dcbeeddc1daf39177-Paper-Conference.pdf)** – injecting 3D features into large language models.
- **[3DMIT (2024)](https://arxiv.org/pdf/2401.03201)** – 3D multi-modal instruction tuning for scene understanding.
- **[EPCL (AAAI 2024)](https://arxiv.org/abs/2212.04098)** – frozen CLIP transformer as efficient point cloud encoder.

# 📝 FDE Field Notes

> **Battle-tested engineering patterns and production lessons from the AI deployment frontlines.**

[![Live Web App](https://img.shields.io/badge/Live%20Site-iggym.github.io%2Ffde--field--notes-brightgreen?style=for-the-badge&logo=github)](https://iggym.github.io/fde-field-notes)
[![GitHub Repository](https://img.shields.io/badge/GitHub-iggym%2Ffde--field--notes-blue?style=for-the-badge&logo=github)](https://github.com/iggym/fde-field-notes/tree/main)
[![Newsletter Archive](https://img.shields.io/badge/Buttondown-FDE%20Field%20Guide-FF6B6B?style=for-the-badge&logo=buttondown)](https://buttondown.com/fdefieldguide/archive)

---

## 🎯 What is FDE Field Notes?

**FDE Field Notes** is a curated collection of real-world insights, architecture patterns, and post-mortems captured directly from Forward Deployed Engineering (FDE) teams deploying AI models into production environments.

> 💬 *"Forward deployed engineering keeps collapsing the distance between **'the model can do this'** and **'this is in production at the customer.'**"* 

Instead of theoretical model benchmarks or synthetic demos, this repository focuses on **the glue code, harness designs, security guardrails, and hardware reality** required to ship working systems.

---

## 👥 Audience: Who Is This For?

| Role | Why You Need This |
| :--- | :--- |
| 🛠️ **Forward Deployed Engineers (FDEs)** | You are on site with customers writing the integration code, prompt harnesses, and fallback pipelines that make models actually work. |
| 🏗️ **AI Infrastructure & Platform Engineers** | You own the operational surface—auth, data residency, sandboxing, rate limiting, and rollback mechanisms. |
| 📐 **Solutions Architects & Tech Leads** | You need empirical evidence on cost, latency, and harness levers before committing client architectures to expensive model swaps. |
| 💼 **Technical Founders & Product Leaders** | You want to understand why deployment strategy and system design around the model dictate product outcomes. |

---

## 💡 The Need: Why Field Notes Matter

In production AI, **the model is only half the equation.** 

> 💬 *"The teams winning treat the deployment surface — auth, data access, evals, rollback — as the product, not an afterthought. If you own that surface, you own the outcome."*

### Key Reality Checks from the Field:
* 🧪 **Harnessing > Model Swapping:** 
  > 💬 *"A **60-82% accuracy swing** on the same 4B model classification task where the only variable was harness design. Prompt formatting, output parsing, and answer extraction moved accuracy more than a model swap would."* — [Read the Analysis](https://buttondown.com/fdefieldguide/archive/fde-field-notes-2026-08-01-5704/)
* 🔒 **Sovereignty & On-Prem Economics:** Sub-$0.18/M near-frontier open weights are enabling fully sovereign on-prem pipelines, but inference engine choice materially shifts throughput on customer hardware.
* ⚙️ **Boring Infrastructure Rules:** Unbatched API calls are now a code-review smell. Tool loops require idempotency, deduplication, and dry-run sandbox modes before touching production databases.

---

## 📖 Key Topics Covered

- 🎨 **Harness & Eval Design:** How to structure prompt pipelines and output extraction to maximize low-parameter model accuracy.
- 🔄 **Agentic Loops & Guardrails:** Transitioning single-prompt callers into resilient tool-using loops.
- ⚡ **Local & On-Prem Hardware Benchmarks:** Real-world throughput testing on client boxes (TensorSharp vs. llama.cpp).
- 🌉 **Multi-Model Integration Glue:** State sharing across Claude and ChatGPT via Model Context Protocol (MCP).
- 🚨 **Production Post-Mortems:** When to keep routing simple, when to deprecate LLM routers, and how to avoid over-engineering.

---

## ⚡ Tech Stack & Principles

This web application is built with extreme minimalism and zero build friction in mind:

- 🎨 **Frontend:** Vanilla HTML5, CSS3, and modern ECMAScript (ES6+)
- 🚀 **Zero Dependencies:** No React, Tailwind, Vite, or npm bundle overhead

---

## 🛠️ Quickstart (Local Development)

Since there are no build steps or dependencies, you can run the application with any standard local web server:

```bash
# 1. Clone the repository
git clone https://github.com/iggym/fde-field-notes.git

# 2. Enter the repository directory
cd fde-field-notes

# 3. Spin up a lightweight local server (Python 3)
python3 -m http.server 8000
```

Then open `http://localhost:8000` in your browser. 🎈

---

## 🚀 Deployment

* **Automatic Deployments:** Any commits or pull requests merged into `main` automatically deploy to [GitHub Pages](https://iggym.github.io/fde-field-notes/).
* **Client-Side Runtime:** All processing runs 100% in the user's browser.

---

## 🤝 Contributing & Feedback

Have field notes, harness benchmarks, or production post-mortems from your own FDE deployments?

1. 🍴 **Fork** the repository
2. 🌿 Create a feature branch (`git checkout -b field-note/my-insight`)
3. ✍️ Draft the article with the [master prompt](docs/master-prompt-v1.md) and add its entry to `metadata.json`
4. 📥 Open a **Pull Request** with your updates!

See [`tasks/tasks.md`](tasks/tasks.md) for the current improvement backlog.

---

---
title: 'Feasibility-Study-App: an open-source Arabic-language platform for integrated economic feasibility studies in agriculture, industry, and renewable energy'
tags:
  - decision support
  - feasibility study
  - agriculture
  - renewable energy
  - monte carlo simulation
  - arabic
authors:
  - name: Abbas Ahmed Mohammed Hebah
    orcid: 0009-0000-5689-2157
    affiliation: 1
affiliations:
  - name: "Sana'a University, Yemen"
    index: 1
date: 17 October 2026
bibliography: paper.bib
---

# Summary

Economic feasibility studies evaluate whether a proposed investment is technically possible and financially justified before capital is committed, and they conventionally combine market, technical, financial, environmental and legal analyses. In practice these components are usually prepared in disconnected documents and spreadsheets. Feasibility-Study-App is an open-source, Arabic-first web and desktop application that integrates the eight conventional study components — foundation, social, environmental, legal, marketing, technical, financial and economic — into a single workflow. Its analytical core is a suite of dependency-free TypeScript financial engines implementing net present value (NPV), internal rate of return (IRR), modified internal rate of return (MIRR) [@kierulff2008], payback period, profitability index and weighted average cost of capital (WACC) [@brealey2020]. Risk is quantified through Monte Carlo simulation of more than 1,000 scenarios [@metropolis1949], tornado sensitivity analysis [@saltelli2008] and probability-weighted scenario comparison, while strategic assessment is supported through SWOT [@learned1965] and Porter's Five Forces [@porter1980] frameworks. Reference libraries tailored to the Yemeni context ship with the application: 34 agricultural crops with scientific specifications, 30 agro-processing factory profiles, 10 renewable energy projects with dedicated solar, wind, hydropower and tariff calculators, 12 editable model projects and a financial glossary. Results export to PDF, PowerPoint, Word, Excel, JSON, HTML and CSV. The application is delivered as a web service, as an offline-capable progressive web app, and as a Windows desktop executable built with Electron, and exposes a REST API for programmatic access.

# Statement of need

Entrepreneurs, cooperatives and small and medium enterprises in resource-constrained economies often commit capital on the basis of intuition rather than structured analysis. Professional feasibility consulting is expensive, and commercial feasibility software is proprietary, English-centric and licensed per seat — barriers that are particularly acute in Arabic-speaking markets. Spreadsheet-based appraisal, meanwhile, demands financial expertise that many project promoters lack, and even experienced analysts must re-implement discounted-cash-flow mechanics from scratch for every project, with the usual risks of transcription and formula errors, rather than relying on tested, reusable engines [@brealey2020].

A second problem is fragmentation: the marketing, technical and financial sections of a feasibility study are typically prepared in isolation, producing internal inconsistencies in documents that are meant to support a single investment decision. To the best of our knowledge, few open-source tools combine the eight study components, embedded local reference datasets and probabilistic risk analysis in a single Arabic-language application. Feasibility-Study-App addresses this gap by pairing integrated study management with unit-tested financial engines, so that appraisal results are reproducible and auditable. The embedded Yemeni crop, factory and renewable energy datasets, the offline-capable mode for low-connectivity environments, and the permissive MIT licence make the tool directly usable by universities, agricultural extension services, cooperatives and individual investors, and adaptable to neighbouring contexts through its open data model.

# Implementation

Feasibility-Study-App is implemented in TypeScript on Next.js 16, with a Tailwind CSS and shadcn/ui interface, Prisma ORM over SQLite for persistence, Recharts for visualisation, and combined Zustand and TanStack Query state management. All financial and statistical engines — NPV, IRR, MIRR, depreciation and tax schedules, weighted scenario analysis, tornado sensitivity and Monte Carlo simulation — are pure, dependency-free TypeScript modules, a design choice that makes them directly unit-testable. The test suite comprises 48 unit tests with 204 assertions covering analytical reference values for every indicator, integration cases for viable and non-viable projects, depreciation and tax table consistency, probability-weighted scenarios, tornado ordering including inversion of the discount-rate branch, and Monte Carlo statistical invariants, including the zero-variance degenerate case that must reproduce the analytic base scenario exactly. The suite executes in continuous integration on every push using the Bun runtime. The application ships as a progressive web app with a service worker for offline use, and a GitHub Actions workflow packages it into a Windows desktop executable with Electron.

# References

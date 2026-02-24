// Credits: Erwin Lejeune — 2026-02-24
import React from "react";
import { createRoot } from "react-dom/client";

import { DocsApp } from "./DocsApp";
import "./styles.css";

createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <DocsApp />
  </React.StrictMode>
);

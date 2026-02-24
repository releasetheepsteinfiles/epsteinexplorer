// Credits: Erwin Lejeune - 2026-02-24
import { defineConfig } from "vitepress";

export default defineConfig({
  title: "EpsteinExplorer Docs",
  description: "Documentation for the EpsteinExplorer application",
  cleanUrls: true,
  themeConfig: {
    logo: "/logo.svg",
    nav: [
      { text: "Home", link: "/" },
      { text: "Getting Started", link: "/guide/getting-started" },
      { text: "Architecture", link: "/guide/architecture" },
      { text: "API", link: "/guide/api" }
    ],
    sidebar: [
      {
        text: "Guide",
        items: [
          { text: "Getting Started", link: "/guide/getting-started" },
          { text: "Architecture", link: "/guide/architecture" },
          { text: "API", link: "/guide/api" }
        ]
      }
    ],
    socialLinks: [{ icon: "github", link: "https://github.com/guilyx/epsteinexplorer" }],
    search: {
      provider: "local"
    }
  }
});

(function () {
  const APIs = {
    node: { label: "Node.js", url: "http://localhost:3000" },
    python: { label: "Python", url: "http://localhost:5000" },
  };

  function getSelected() {
    return localStorage.getItem("api_backend") || "python";
  }

  function setSelected(name) {
    if (!APIs[name]) return;
    localStorage.setItem("api_backend", name);
    window.dispatchEvent(new CustomEvent("api-backend-changed"));
  }

  function getBaseUrl() {
    return APIs[getSelected()].url;
  }

  function renderSelector() {
    const old = document.getElementById("api-selector");
    if (old) return;
    const box = document.createElement("div");
    box.id = "api-selector";
    box.style.cssText = "position:fixed;right:16px;bottom:16px;z-index:9999;background:#0b1730;color:white;padding:10px 12px;border:1px solid #3498db;border-radius:10px;font:14px Arial;box-shadow:0 4px 16px #0005";
    box.innerHTML = '<label for="api-backend">API: </label><select id="api-backend" style="padding:4px;border-radius:5px"><option value="node">Node.js (3000)</option><option value="python">Python (5000)</option></select>';
    document.body.appendChild(box);
    const select = box.querySelector("select");
    select.value = getSelected();
    select.addEventListener("change", () => { setSelected(select.value); location.reload(); });
  }

  window.API_CONFIG = { APIs, getSelected, setSelected, getBaseUrl, renderSelector };
  document.addEventListener("DOMContentLoaded", renderSelector);
})();

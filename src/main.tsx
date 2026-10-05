import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "leaflet/dist/leaflet.css";
import { App } from "./App";
import { DriverApp } from "./components/driver/DriverApp";
import { Tracking } from "./pages/Tracking";
import "./index.css";

const root = document.getElementById("root");
if (!root) {
  throw new Error("No se encontró el nodo raíz.");
}

const path = window.location.pathname;

createRoot(root).render(
  <StrictMode>
    {path.startsWith("/conductor") ? <DriverApp /> : path.startsWith("/seguimiento") ? <Tracking /> : <App />}
  </StrictMode>,
);

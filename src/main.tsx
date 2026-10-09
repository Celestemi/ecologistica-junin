import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "leaflet/dist/leaflet.css";
import { App } from "./App";
import { DriverApp } from "./components/driver/DriverApp";
import { homeFor, screenAllowed } from "./lib/access";
import { loadSession } from "./lib/session";
import { AuditLog } from "./pages/AuditLog";
import { Fleet } from "./pages/Fleet";
import { Login } from "./pages/Login";
import { OrdersDay } from "./pages/OrdersDay";
import { Tracking } from "./pages/Tracking";
import "./index.css";

const root = document.getElementById("root");
if (!root) {
  throw new Error("No se encontró el nodo raíz.");
}

function Root() {
  const path = window.location.pathname;
  if (path.startsWith("/seguimiento")) {
    return <Tracking />;
  }
  if (path.startsWith("/ingresar")) {
    return <Login />;
  }
  const session = loadSession();
  if (!session) {
    const next = `${path}${window.location.search}`;
    window.location.replace(`/ingresar?siguiente=${encodeURIComponent(next)}`);
    return null;
  }
  const rol = session.usuario.rol;
  if (!screenAllowed(rol, path)) {
    window.location.replace(homeFor(rol));
    return null;
  }
  if (path.startsWith("/auditoria")) {
    return <AuditLog />;
  }
  if (path.startsWith("/pedidos")) {
    return <OrdersDay />;
  }
  if (path.startsWith("/flota")) {
    return <Fleet />;
  }
  if (path.startsWith("/conductor")) {
    return <DriverApp />;
  }
  return <App />;
}

createRoot(root).render(
  <StrictMode>
    <Root />
  </StrictMode>,
);

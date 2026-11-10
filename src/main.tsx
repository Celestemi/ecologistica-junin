import { lazy, StrictMode, Suspense } from "react";
import { createRoot } from "react-dom/client";
import "leaflet/dist/leaflet.css";
import { homeFor, screenAllowed } from "./lib/access";
import { loadSession } from "./lib/session";
import "./index.css";

const App = lazy(() => import("./App").then((module) => ({ default: module.App })));
const DriverApp = lazy(() => import("./components/driver/DriverApp").then((module) => ({ default: module.DriverApp })));
const AuditLog = lazy(() => import("./pages/AuditLog").then((module) => ({ default: module.AuditLog })));
const Fleet = lazy(() => import("./pages/Fleet").then((module) => ({ default: module.Fleet })));
const PlateRestrictions = lazy(() => import("./pages/PlateRestrictions").then((module) => ({ default: module.PlateRestrictions })));
const Login = lazy(() => import("./pages/Login").then((module) => ({ default: module.Login })));
const OrdersDay = lazy(() => import("./pages/OrdersDay").then((module) => ({ default: module.OrdersDay })));
const Tracking = lazy(() => import("./pages/Tracking").then((module) => ({ default: module.Tracking })));

if (import.meta.env.PROD && "serviceWorker" in navigator) {
  window.addEventListener("load", () => {
    void navigator.serviceWorker.register("/sw.js").catch((error: unknown) => {
      console.warn("No se pudo activar el soporte offline.", error);
    });
  });
}

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
  if (path.startsWith("/flota/restricciones-placa")) {
    return <PlateRestrictions />;
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
    <Suspense fallback={<div className="min-h-screen bg-[#f3efe6] p-4 text-stone-900" role="status">Cargando…</div>}>
      <Root />
    </Suspense>
  </StrictMode>,
);

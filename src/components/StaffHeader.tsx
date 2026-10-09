import { useState } from "react";
import { ApiError, downloadSustainabilityPdf } from "../api";
import { canAudit, canDownloadReport, canDrive, canOpenDispatch, canSeeDesk } from "../lib/access";
import { loadSession } from "../lib/session";
import { Brand } from "./Brand";
import { SessionMenu } from "./SessionMenu";

type StaffHeaderProps = {
  title: string;
  tone?: "paper" | "field";
};

export function StaffHeader({ title, tone = "paper" }: StaffHeaderProps) {
  const session = loadSession();
  const [reportError, setReportError] = useState<string | null>(null);
  const [downloading, setDownloading] = useState(false);
  if (!session) {
    return null;
  }
  const rol = session.usuario.rol;
  const path = window.location.pathname;
  const field = tone === "field";
  const chip = field
    ? "inline-flex min-h-11 items-center rounded-full bg-white/15 px-3 text-sm font-semibold text-white"
    : "inline-flex min-h-11 items-center rounded-full bg-emerald-50 px-3 text-sm font-semibold text-emerald-950 hover:bg-emerald-100";
  const solid = field
    ? chip
    : "inline-flex min-h-11 items-center rounded-full bg-[#14532d] px-3 text-sm font-semibold text-white hover:bg-emerald-950";

  async function onReport() {
    setDownloading(true);
    setReportError(null);
    try {
      await downloadSustainabilityPdf();
    } catch (reason: unknown) {
      setReportError(reason instanceof ApiError ? reason.message : "No se pudo descargar el informe.");
    } finally {
      setDownloading(false);
    }
  }

  return (
    <header
      className={
        field
          ? "sticky top-0 z-10 border-b border-emerald-950 bg-[#14532d] px-4 py-3 text-white"
          : "border-b border-stone-200 bg-white/80 px-4 py-3"
      }
    >
      <div className={`flex flex-wrap items-center justify-between gap-3 ${field ? "mx-auto max-w-lg" : ""}`}>
        <Brand light={field} title={title} />
        <nav className="flex flex-wrap items-center gap-2" aria-label="Secciones de tu rol">
          {canOpenDispatch(rol) && path !== "/" ? (
            <a className={chip} href="/">
              Despacho
            </a>
          ) : null}
          {canSeeDesk(rol) && !path.startsWith("/pedidos") ? (
            <a className={chip} href="/pedidos">
              Pedidos
            </a>
          ) : null}
          {canSeeDesk(rol) && !path.startsWith("/flota") ? (
            <a className={chip} href="/flota">
              Flota
            </a>
          ) : null}
          {canDrive(rol) && !path.startsWith("/conductor") ? (
            <a className={solid} href="/conductor">
              Modo conductor
            </a>
          ) : null}
          {canAudit(rol) && !path.startsWith("/auditoria") ? (
            <a className={chip} href="/auditoria">
              Bitácora
            </a>
          ) : null}
          {canDownloadReport(rol) ? (
            <button type="button" className={chip} disabled={downloading} onClick={() => void onReport()}>
              {downloading ? "Preparando informe…" : "Informe PDF"}
            </button>
          ) : null}
          <SessionMenu light={field} />
        </nav>
      </div>
      {reportError ? (
        <p className={field ? "mt-2 text-sm text-amber-100" : "mt-2 text-sm text-rose-800"}>{reportError}</p>
      ) : null}
    </header>
  );
}

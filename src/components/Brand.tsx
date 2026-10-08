type BrandProps = {
  light?: boolean;
  title: string;
};

export function Brand({ light = false, title }: BrandProps) {
  return (
    <div className="flex items-center gap-3">
      <span
        className={`flex h-10 w-10 items-center justify-center rounded-2xl ${
          light ? "bg-white/15 text-white" : "bg-[#14532d] text-white"
        }`}
        aria-hidden="true"
      >
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none">
          <path
            d="M12 21s7-5.4 7-11a7 7 0 1 0-14 0c0 5.6 7 11 7 11Z"
            stroke="currentColor"
            strokeWidth="1.8"
          />
          <path d="M12 14c2-2.4 3-4.2 3-6" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" />
        </svg>
      </span>
      <div>
        <p className={`text-[11px] font-semibold tracking-[0.16em] ${light ? "text-emerald-100" : "text-emerald-900/70"}`}>
          VALLE DEL MANTARO
        </p>
        <h1 className="text-lg font-semibold leading-tight">{title}</h1>
      </div>
    </div>
  );
}

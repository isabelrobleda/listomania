/**
 * The progress bar is the same marker stroke that sits under every heading —
 * one gesture doing both branding and data, drawn to the percentage complete.
 */
export default function StrokeBar({
  color,
  pct,
  height = 15,
}: {
  color: string;
  pct: number;
  height?: number;
}) {
  const d = `M5 ${height * 0.62} C 110 ${height * 0.34}, 300 ${height * 0.72}, 495 ${height * 0.4}`;
  const w = height * 0.72;
  return (
    <svg
      className="strokebar"
      viewBox={`0 0 500 ${height}`}
      preserveAspectRatio="none"
      aria-hidden="true"
      style={{ height }}
    >
      <path d={d} stroke="var(--line)" strokeWidth={w} />
      <path
        d={d}
        stroke={color}
        strokeWidth={w}
        pathLength={100}
        strokeDasharray={`${pct} 100`}
      />
    </svg>
  );
}

/** The marker stroke behind a heading. */
export function Underline({ color, size = 40 }: { color: string; size?: number }) {
  return (
    <svg viewBox={`0 0 300 ${size}`} preserveAspectRatio="none" aria-hidden="true">
      <path
        d={`M4 ${size * 0.66} C 80 ${size * 0.5}, 200 ${size * 0.6}, 296 ${size * 0.46}`}
        stroke={color}
        strokeWidth={size * 0.55}
      />
    </svg>
  );
}

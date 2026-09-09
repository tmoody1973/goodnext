import type { HelpRoute } from "@/lib/api";
import { copy, fill } from "@/lib/copy";
import { telHref } from "@/lib/phone";
import { textLinkClass } from "@/lib/styles";

// CONTEXT.md "Help route": a maintained, verified way to reach a human. The
// list comes only from the API's reviewed constant, never from this site.
export function HelpRoutes({ routes }: { routes: HelpRoute[] }) {
  if (routes.length === 0) return null;
  return (
    <section aria-labelledby="help-heading" className="flex flex-col gap-3 rounded-2xl border border-line px-4 py-4">
      <h2 id="help-heading" className="text-lg font-semibold">{copy.help.heading}</h2>
      <ul className="flex flex-col gap-3">
        {routes.map((r) => {
          const tel = r.phone ? telHref(r.phone) : null;
          return (
            <li key={r.name} className="flex flex-col gap-0.5">
              <p className="font-semibold">{r.name}</p>
              <p>{r.purpose}</p>
              <p className="flex flex-wrap gap-x-4">
                {r.phone && (tel ? (
                  <a href={tel} className={textLinkClass}>{r.phone}</a>
                ) : (
                  <span className="font-medium">{r.phone}</span>
                ))}
                {r.url && (
                  <a href={r.url} target="_blank" rel="noopener noreferrer" className={`${textLinkClass} [overflow-wrap:anywhere]`}>
                    {new URL(r.url).hostname}
                  </a>
                )}
              </p>
              <p className="text-xs text-ink-soft">{fill(copy.help.checked, { date: r.last_checked })}</p>
            </li>
          );
        })}
      </ul>
    </section>
  );
}

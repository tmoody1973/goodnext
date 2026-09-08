import type { Metadata } from "next";
import "./globals.css";
import { copy } from "@/lib/copy";

export const metadata: Metadata = {
  title: copy.site.name,
  description: copy.site.description,
};

// Impeccable direction contract (decision 007, seed a5fbc27f). Emitted as a real
// HTML comment inside an inert <template> so it survives the static build and
// can be audited with grep. Nothing renders from it.
const directionContract = `<!--
THESIS: Today is the big panel; the next six days are small tiles. Refuses the civic-portal list of same-size cards.
OWN-WORLD: navy header field, white cards, amber only where something can be pressed or counted; system sans; status in words, color secondary.
STORY: a resident sees the date and how many places are listed today, reads each card's opening window first, taps Directions; later days are visibly not promises.
FIRST VIEWPORT: wordmark and "Not a government service"; the four-question form; on result, the navy panel with the date and "N listed today", then cards with the time block left.
FORM: The 7-Day Forecast Strip, candidate 1 of 7 (Impeccable's pick over the rolled candidate 5); seed a5fbc27f.
FINISH: unreviewed and undocumented is unfinished; this build ends with the finish review, the verdict, DESIGN.md, and every shipping raster carrying its provenance.
-->`;

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className="h-full antialiased">
      <body className="min-h-full flex flex-col bg-paper text-ink">
        <template
          id="direction-contract"
          dangerouslySetInnerHTML={{ __html: directionContract }}
        />
        {children}
      </body>
    </html>
  );
}

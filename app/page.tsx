import Link from "next/link";
import { shelves } from "@/lib/content";
import Stats from "@/components/Stats";
import { ListLine, MyListLine } from "@/components/Directory";

/**
 * The home page is a directory, not a showcase.
 *
 * Cards looked good and scaled badly: five shelves of cards already pushed the
 * newest lists below the fold, and every list added makes that worse. The
 * craigslist move is to treat the front page as an index — every destination
 * visible at once, in columns, as plain links — so the page gets *denser* as it
 * grows rather than longer. The only decoration is the shelf's colour, and the
 * counts, which are the actual information.
 */
export default function Home() {
  return (
    <>
      <section className="clhead">
        <div>
          <h1>An encyclopedia of lists</h1>
          <p>
            Canons, crowd tallies and things to get through. Tick what you&rsquo;ve done, bookmark
            what you want — every list says where it came from and how it was counted.
          </p>
        </div>
        <Stats />
      </section>

      <div className="cl">
        {shelves.map((shelf) => (
          <section className="clsec" key={shelf.slug} style={{ ["--mark" as string]: shelf.mark }}>
            <h2>
              <Link href={`/${shelf.slug}`}>
                <span className="dot" />
                {shelf.name}
              </Link>
            </h2>
            <p className="clblurb">{shelf.blurb}</p>
            <ul>
              {shelf.lists.map((list) => (
                <ListLine key={list.slug} shelf={shelf} list={list} />
              ))}
              {shelf.lists.length === 0 && <li className="empty">nothing here yet</li>}
              <MyListLine shelf={shelf} />
            </ul>
          </section>
        ))}

        <section className="clsec soon">
          <h2>
            <span className="dot" />
            Coming next
          </h2>
          <p className="clblurb">Shelves with nothing on them yet.</p>
          <ul>
            {["Talks & video", "Podcasts", "Games", "Recipes"].map((n) => (
              <li key={n}>
                <span className="soonline">{n}</span>
              </li>
            ))}
          </ul>
        </section>
      </div>

      <p className="note">
        <b>How this works.</b> The lists live in the repository as data files, so every change to
        one is a visible, reviewable edit rather than an invisible database write. What you tick and
        what you bookmark stay in this browser — there are no accounts yet.
      </p>
    </>
  );
}

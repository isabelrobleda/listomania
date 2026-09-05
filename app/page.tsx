import Link from "next/link";
import { shelves } from "@/lib/content";
import Stats from "@/components/Stats";
import { ListLine } from "@/components/Directory";
import MyLists from "@/components/MyLists";

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
        <MyLists />

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
            {["Talks & video", "Games", "Recipes"].map((n) => (
              <li key={n}>
                <span className="soonline">{n}</span>
              </li>
            ))}
          </ul>
        </section>
      </div>

      {/* Same three columns as the directory above, so the notes read as the
          bottom of that grid rather than as one narrow orphan column. Full
          width with a single measure would be a ~200-character line on a big
          monitor, which is the one typography rule worth keeping. */}
      <div className="clnotes">
      <p className="note">
        <b>How this works.</b> Two marks per row, and they mean different things: the tick on the
        left is <b>I&rsquo;ve read / seen / been there</b>, the bookmark on the right is{" "}
        <b>put it on my list</b> — you can want to reread something you&rsquo;ve already finished.
        Saved rows collect on one page per shelf, one copy each however many lists recommended
        them. All of it lives in this browser until you make an account, and then it follows you
        between devices; an account is a username and a password and nothing else, with no email
        address stored on either sign-in path.
      </p>
      <p className="note">
        <b>Where the lists come from.</b> They&rsquo;re data files in a public repository, not rows
        in a database, so every change to a list is a visible edit someone can argue with. Each one
        says who was asked, where, and how the answers were counted — including what the count
        can&rsquo;t tell you. That last part is the whole point:{" "}
        <a href="https://github.com/isabelrobleda/listomania" target="_blank" rel="noopener noreferrer">
          the source is here
        </a>
        .
      </p>
      </div>
    </>
  );
}

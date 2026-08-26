import { shelves } from "@/lib/content";
import { Underline } from "@/components/StrokeBar";
import ListCard from "@/components/ListCard";
import Stats, { ShelfCount } from "@/components/Stats";

export default function Home() {
  return (
    <>
      <section className="hero">
        <h1>
          Everything worth listing,
          <br />
          in one place.
        </h1>
        <p>
          Canons, tallies and things to get through — kept as lists you can actually work your way
          down. Mark items off as you go; the counts follow you.
        </p>
        <Stats />
      </section>

      {shelves.map((shelf) => (
        <section className="shelf" key={shelf.slug}>
          <div className="shelfhead">
            <h2>
              <span className="mk">
                <Underline color={shelf.mark} size={30} />
                <span className="w">{shelf.name}</span>
              </span>
            </h2>
            <ShelfCount slug={shelf.slug} />
          </div>
          <p className="shelfblurb">{shelf.blurb}</p>
          <div className="grid">
            {shelf.lists.map((list) => (
              <ListCard key={list.slug} shelf={shelf} list={list} />
            ))}
          </div>
        </section>
      ))}

      <p className="note">
        <b>Progress is saved in this browser.</b> There are no accounts yet — what you mark off
        stays on this device. The lists themselves live in the repository as data files, so every
        change to them is a visible, reviewable edit rather than an invisible database write.
      </p>
    </>
  );
}

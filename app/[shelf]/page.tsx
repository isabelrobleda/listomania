import { notFound } from "next/navigation";
import Link from "next/link";
import { shelves, getShelf } from "@/lib/content";
import { Underline } from "@/components/StrokeBar";
import ListCard from "@/components/ListCard";
import ShelfProgress from "@/components/ShelfProgress";
import ShelfTheme from "@/components/ShelfTheme";

export function generateStaticParams() {
  return shelves.map((s) => ({ shelf: s.slug }));
}

export async function generateMetadata({ params }: { params: Promise<{ shelf: string }> }) {
  const shelf = getShelf((await params).shelf);
  if (!shelf) return {};
  return { title: `${shelf.name} — Listomania`, description: shelf.blurb };
}

export default async function ShelfPage({ params }: { params: Promise<{ shelf: string }> }) {
  const shelf = getShelf((await params).shelf);
  if (!shelf) notFound();

  return (
    <>
      <ShelfTheme shelf={shelf} />
      <nav className="crumbs" aria-label="Breadcrumb">
        <Link href="/">Everything</Link>
        <span aria-hidden="true">/</span>
        <b>{shelf.name}</b>
      </nav>

      <div className="lhead">
        <div>
          <h1>
            <span className="mk">
              <Underline color={shelf.mark} />
              <span className="w">{shelf.name}</span>
            </span>
          </h1>
          <p>{shelf.blurb}</p>
        </div>
        {shelf.lists.length > 0 && <ShelfProgress shelf={shelf} />}
      </div>

      {/* Both chips show even on a shelf with no lists on it yet: your own
          favourites don't depend on there being a crowd to disagree with. */}
      <div className="tools">
        <Link className="chip" href={`/${shelf.slug}/my-list`}>
          My {shelf.name.toLowerCase()} list
        </Link>
        <Link className="chip" href={`/${shelf.slug}/my-favourites`}>
          + Add your own
        </Link>
      </div>

      {shelf.lists.length === 0 ? (
        <p className="note" style={{ marginTop: 22 }}>
          <b>Nothing on this shelf yet.</b> The list that was here has been
          retired, and its replacement is being built.
        </p>
      ) : (
        <div className="grid" style={{ marginTop: 22 }}>
          {shelf.lists.map((list) => (
            <ListCard key={list.slug} shelf={shelf} list={list} />
          ))}
        </div>
      )}
    </>
  );
}

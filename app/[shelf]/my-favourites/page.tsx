import { notFound } from "next/navigation";
import { shelves, getShelf } from "@/lib/content";
import ShelfTheme from "@/components/ShelfTheme";
import OwnList from "@/components/OwnList";

export function generateStaticParams() {
  return shelves.map((s) => ({ shelf: s.slug }));
}

export async function generateMetadata({ params }: { params: Promise<{ shelf: string }> }) {
  const shelf = getShelf((await params).shelf);
  if (!shelf) return {};
  return {
    title: `My ${shelf.name.toLowerCase()} favourites — Listomania`,
    description: `The things you added yourself to the ${shelf.name} shelf.`,
    // Nothing here exists until someone writes it, and it's theirs, not the web's.
    robots: { index: false, follow: true },
  };
}

export default async function MyFavouritesPage({ params }: { params: Promise<{ shelf: string }> }) {
  const shelf = getShelf((await params).shelf);
  if (!shelf) notFound();

  return (
    <>
      <ShelfTheme shelf={shelf} />
      <OwnList shelf={shelf} />
    </>
  );
}

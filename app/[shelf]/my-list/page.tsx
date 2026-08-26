import { notFound } from "next/navigation";
import { shelves, getShelf } from "@/lib/content";
import ShelfTheme from "@/components/ShelfTheme";
import SavedList from "@/components/SavedList";

export function generateStaticParams() {
  return shelves.map((s) => ({ shelf: s.slug }));
}

export async function generateMetadata({ params }: { params: Promise<{ shelf: string }> }) {
  const shelf = getShelf((await params).shelf);
  if (!shelf) return {};
  return {
    title: `My ${shelf.name.toLowerCase()} list — Listomania`,
    description: `Everything you've saved from the ${shelf.name} shelf.`,
    // Nothing here exists until someone saves something, so there's nothing to index.
    robots: { index: false, follow: true },
  };
}

export default async function MyListPage({ params }: { params: Promise<{ shelf: string }> }) {
  const shelf = getShelf((await params).shelf);
  if (!shelf) notFound();

  return (
    <>
      <ShelfTheme shelf={shelf} />
      <SavedList shelf={shelf} />
    </>
  );
}

import { notFound } from "next/navigation";
import Link from "next/link";
import { shelves, getList } from "@/lib/content";
import ListTable from "@/components/ListTable";
import ShelfTheme from "@/components/ShelfTheme";

export function generateStaticParams() {
  return shelves.flatMap((s) => s.lists.map((l) => ({ shelf: s.slug, list: l.slug })));
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ shelf: string; list: string }>;
}) {
  const p = await params;
  const found = getList(p.shelf, p.list);
  if (!found) return {};
  return { title: `${found.list.title} — Listomania`, description: found.list.desc };
}

export default async function ListPage({
  params,
}: {
  params: Promise<{ shelf: string; list: string }>;
}) {
  const p = await params;
  const found = getList(p.shelf, p.list);
  if (!found) notFound();
  const { shelf, list } = found;

  return (
    <>
      <ShelfTheme shelf={shelf} />
      <nav className="crumbs" aria-label="Breadcrumb">
        <Link href="/">Everything</Link>
        <span aria-hidden="true">/</span>
        <Link href={`/${shelf.slug}`}>{shelf.name}</Link>
        <span aria-hidden="true">/</span>
        <b>{list.title}</b>
      </nav>
      <ListTable shelf={shelf} list={list} />
    </>
  );
}

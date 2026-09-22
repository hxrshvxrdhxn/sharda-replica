export const dynamic = "force-dynamic";

interface PageProps {
  params: Promise<{
    slug?: string[];
  }>;
}

export default async function UniversalDynamicPage({ params }: PageProps) {
  const resolvedParams = await params;
  const slugArray = resolvedParams?.slug || [];
  const fullSlug = slugArray.join("/");

  let htmlContent = "";
  try {
    const res = await fetch(`http://127.0.0.1:8000/replica/${fullSlug}`, {
      cache: "no-store",
    });
    if (res.ok) {
      htmlContent = await res.text();
    }
  } catch (e) {
    console.error("Error fetching replica page:", e);
  }

  if (!htmlContent) {
    return (
      <div className="min-h-screen bg-[#1B2C39] text-white flex flex-col items-center justify-center p-6 text-center">
        <h1 className="text-3xl font-bold mb-4">Sharda University</h1>
        <p className="text-gray-300 max-w-md mb-6">
          The requested university page is being loaded from the central catalog.
        </p>
        <a
          href="/"
          className="bg-[#EAA914] text-[#1B2C39] font-bold px-6 py-3 rounded-xl uppercase text-xs tracking-wider"
        >
          Return to Home
        </a>
      </div>
    );
  }

  return (
    <div
      dangerouslySetInnerHTML={{ __html: htmlContent }}
      style={{ width: "100%", minHeight: "100vh" }}
    />
  );
}

import fs from "fs";
import path from "path";

export const dynamic = "force-dynamic";

export default async function HomePage() {
  let htmlContent = "";
  try {
    const res = await fetch("http://127.0.0.1:8000/replica/", {
      cache: "no-store",
    });
    if (res.ok) {
      htmlContent = await res.text();
    }
  } catch (e) {
    console.error("Error fetching replica root:", e);
  }

  if (!htmlContent) {
    const htmlPath = path.join(process.cwd(), "public", "index_replica.html");
    try {
      htmlContent = fs.readFileSync(htmlPath, "utf-8");
    } catch (e) {
      htmlContent = "<h1>Loading Sharda University Replica...</h1>";
    }
  }

  return (
    <div
      dangerouslySetInnerHTML={{ __html: htmlContent }}
      style={{ width: "100%", minHeight: "100vh" }}
    />
  );
}


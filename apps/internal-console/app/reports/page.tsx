import { getFieldPackets } from "@/modules/api-client";
import { ReportExporter } from "./exporter";

export default async function ReportsPage() {
  const packets = await getFieldPackets();

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-earth-green">Reports</h1>
        <p className="mt-1 text-sm text-earth-charcoal/70">
          Generate a Markdown Field Packet report. The report runs the mock agent
          pipeline and includes a sensitivity note; it never contains raw coordinates.
        </p>
      </div>

      <ReportExporter packets={packets} />
    </div>
  );
}

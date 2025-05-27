import React, { useState, useEffect, useRef } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip } from "recharts";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import html2canvas from "html2canvas";
import jsPDF from "jspdf";
import Papa from "papaparse";

/**
 * IntegratedDashboardUI displays marketing, sales and subcontractor data.
 */
export function IntegratedDashboardUI() {
  const backendData = {
    marketing: [
      {
        name: "Alice",
        channel: "Facebook Ads",
        campaigns: [
          {
            name: "Winter Promo",
            budget: 10000,
            reach: 100000,
            revenue: 13000,
            roi: 30,
            date: "2024-01",
          },
        ],
        alerts: [],
      },
      {
        name: "Bob",
        channel: "Google SEO",
        campaigns: [
          {
            name: "Spring Blast",
            budget: 15000,
            reach: 120000,
            revenue: 14000,
            roi: -6.7,
            date: "2024-02",
          },
        ],
        alerts: ["\u26A0\uFE0F Campaign 'Spring Blast' flagged for negative ROI: -6.70%"],
      },
    ],
    sales: [
      {
        name: "Jane",
        region: "North",
        leads: [
          { client: "Homeowner A", type: "Roofing", timestamp: "2024-01-05T13:45:00" },
        ],
        deals: [
          { client: "Homeowner A", amount: 18000, job_id: "J001", date: "2024-01" },
        ],
        total_revenue: 18000,
      },
    ],
    subcontractors: [
      {
        name: "Jake",
        trade: "Drywall",
        contact: "555-1234",
        rate: 40,
        permissions: "view_only",
        hours_logged: 15,
        jobs: [{ job_id: "J001", hours: 15 }],
        total_cost: 600,
      },
    ],
  };

  return (
    <div className="p-4 space-y-6">
      <h1 className="text-3xl font-bold">Full System Dashboard</h1>
      <Tabs defaultValue="marketing">
        <TabsList>
          <TabsTrigger value="marketing">Marketing</TabsTrigger>
          <TabsTrigger value="sales">Sales</TabsTrigger>
          <TabsTrigger value="subcontractors">Subcontractors</TabsTrigger>
        </TabsList>

        <TabsContent value="marketing">
          {backendData.marketing.map((rep) => (
            <div key={rep.name} className="mb-6">
              <h2 className="text-lg font-bold mb-2">
                {rep.name} – {rep.channel}
              </h2>
              <LineChart width={600} height={300} data={rep.campaigns}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Line type="monotone" dataKey="budget" stroke="#8884d8" name="Budget" />
                <Line type="monotone" dataKey="revenue" stroke="#82ca9d" name="Revenue" />
                <Line type="monotone" dataKey="roi" stroke="#ff7300" name="ROI %" />
              </LineChart>
              {rep.alerts.length > 0 && (
                <ul className="mt-2 text-red-600 list-disc pl-5">
                  {rep.alerts.map((alert, i) => (
                    <li key={i}>{alert}</li>
                  ))}
                </ul>
              )}
            </div>
          ))}
        </TabsContent>

        <TabsContent value="sales">
          {backendData.sales.map((rep) => (
            <Card key={rep.name} className="mb-4">
              <CardContent className="p-4">
                <p className="text-xl font-bold">
                  {rep.name} – {rep.region}
                </p>
                <p>Total Revenue: ${rep.total_revenue}</p>
                <ul className="mt-2 list-disc pl-5">
                  {rep.deals.map((d, i) => (
                    <li key={i}>
                      {d.client} closed ${d.amount} on {d.date}
                    </li>
                  ))}
                </ul>
              </CardContent>
            </Card>
          ))}
        </TabsContent>

        <TabsContent value="subcontractors">
          {backendData.subcontractors.map((sub) => (
            <Card key={sub.name} className="mb-4">
              <CardContent className="p-4">
                <p className="text-xl font-bold">
                  {sub.name} – {sub.trade}
                </p>
                <p>Contact: {sub.contact}</p>
                <p>Hours Logged: {sub.hours_logged} hrs</p>
                <p>Total Cost: ${sub.total_cost}</p>
              </CardContent>
            </Card>
          ))}
        </TabsContent>
      </Tabs>
    </div>
  );
}

/**
 * ExecutiveDashboardUI shows company-level metrics and alerts.
 */
export function ExecutiveDashboardUI() {
  const [metrics] = useState({
    totalJobs: 32,
    totalBudget: 950000,
    totalSpent: 730000,
    avgProfitMargin: 23.2,
  });
  const [alerts] = useState([
    "\u26A0\uFE0F Job 112 has margin below 15%",
    "\u26A0\uFE0F Subcontractor Jack logged time to unassigned job",
  ]);
  const [marketingChart] = useState([
    { date: "2024-01", budget: 10000, revenue: 14000, roi: 40 },
    { date: "2024-02", budget: 12000, revenue: 11000, roi: -8.3 },
    { date: "2024-03", budget: 15000, revenue: 19000, roi: 26.7 },
  ]);

  return (
    <div className="p-4 space-y-6">
      <h1 className="text-3xl font-bold">Executive Dashboard</h1>
      <Tabs defaultValue="metrics">
        <TabsList>
          <TabsTrigger value="metrics">Company Metrics</TabsTrigger>
          <TabsTrigger value="alerts">Alerts</TabsTrigger>
          <TabsTrigger value="marketing">Marketing ROI</TabsTrigger>
        </TabsList>

        <TabsContent value="metrics">
          <div className="grid grid-cols-2 gap-4">
            <Card>
              <CardContent className="p-4">
                <p className="text-sm">Total Jobs</p>
                <p className="text-xl font-semibold">{metrics.totalJobs}</p>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="p-4">
                <p className="text-sm">Total Budget</p>
                <p className="text-xl font-semibold">
                  ${metrics.totalBudget.toLocaleString()}
                </p>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="p-4">
                <p className="text-sm">Total Spent</p>
                <p className="text-xl font-semibold">
                  ${metrics.totalSpent.toLocaleString()}
                </p>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="p-4">
                <p className="text-sm">Avg Profit Margin</p>
                <p className="text-xl font-semibold">{metrics.avgProfitMargin}%</p>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="alerts">
          <div className="space-y-2">
            {alerts.map((alert, index) => (
              <Card key={index} className="border-red-500">
                <CardContent className="p-4 text-red-700 font-semibold">
                  {alert}
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        <TabsContent value="marketing">
          <LineChart width={600} height={300} data={marketingChart}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" />
            <YAxis />
            <Tooltip />
            <Line type="monotone" dataKey="budget" stroke="#8884d8" name="Budget" />
            <Line type="monotone" dataKey="revenue" stroke="#82ca9d" name="Revenue" />
            <Line type="monotone" dataKey="roi" stroke="#ff7300" name="ROI %" />
          </LineChart>
        </TabsContent>
      </Tabs>
      <Button variant="outline" className="mt-4">
        Refresh Dashboard
      </Button>
    </div>
  );
}


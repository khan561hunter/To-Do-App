"use client";

import { useEffect, useState } from "react";
import { useRouter, usePathname } from "next/navigation";
import { getAuthToken, logout } from "@/auth/better-auth.config";

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const router = useRouter();
  const pathname = usePathname();
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = getAuthToken();
    if (!token && pathname !== "/login" && pathname !== "/register") {
      router.push("/login");
    } else {
      setLoading(false);
    }
  }, [router, pathname]);

  if (loading) {
    return <div className="flex min-h-screen items-center justify-center font-medium">Checking authentication...</div>;
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white border-b px-4 py-3 flex justify-between items-center">
        <h2 className="font-bold text-lg">Todo App</h2>
        <button
          onClick={logout}
          className="text-sm font-medium text-gray-600 hover:text-red-600"
        >
          Logout
        </button>
      </nav>
      <main className="max-w-4xl mx-auto py-8 px-4">
        {children}
      </main>
    </div>
  );
}

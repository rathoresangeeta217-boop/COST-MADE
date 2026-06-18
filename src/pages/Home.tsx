import { Link } from 'react-router-dom';
import { PRODUCTS } from '../types';
import { ChevronRight } from 'lucide-react';

export default function Home() {
  return (
    <div className="space-y-8 animate-in fade-in zoom-in-95 duration-500">
      <div className="max-w-2xl">
        <h1 className="text-3xl font-semibold tracking-tight text-gray-900">Select a Product</h1>
        <p className="mt-2 text-gray-600">
          Choose a furniture product from the catalog to configure its specifications and estimate manufacturing costs.
        </p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        {PRODUCTS.map((product) => (
          <Link
            key={product.id}
            to={product.path}
            className="group flex flex-col bg-white rounded-2xl border border-gray-200 overflow-hidden hover:border-indigo-300 hover:shadow-lg hover:shadow-indigo-100 transition-all duration-200"
          >
            <div className="aspect-[4/3] w-full overflow-hidden bg-gray-100">
              <img
                src={product.imageUrl}
                alt={product.name}
                className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
              />
            </div>
            <div className="p-5 flex-1 flex flex-col">
              <div className="flex items-center justify-between mb-2">
                <h2 className="text-lg font-semibold text-gray-900">{product.name}</h2>
                <div className="w-8 h-8 rounded-full bg-gray-50 flex items-center justify-center text-gray-400 group-hover:bg-indigo-50 group-hover:text-indigo-600 transition-colors">
                  <ChevronRight className="w-4 h-4" />
                </div>
              </div>
              <p className="text-sm text-gray-500 flex-1 leading-relaxed">
                {product.description}
              </p>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}

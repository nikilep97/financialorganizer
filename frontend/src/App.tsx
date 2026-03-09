import { useState } from 'react'

interface Transaction {
  date: string
  description: string
  amount: string
  category: string
}

interface Summary {
  category: string
  total: string
}

interface CategorizedData {
  transactions: Transaction[]
  summary: Summary[]
}

export default function App() {
  const [data, setData] = useState<CategorizedData | null>(null)
  const [loading, setLoading] = useState(false)
  const [file, setFile] = useState<File | null>(null)

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0])
    }
  }

  const analyzeFile = async () => {
    if (!file) return
    setLoading(true)
    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await fetch('/api/categorize', {
        method: 'POST',
        body: formData
      })
      const result = await response.json()
      setData(result)
    } catch (error) {
      console.error('Virhe', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-[#222222] p-8 text-[#c2dbc4]">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold mb-8 text-center">Talouskategorisoija</h1>

        <div className="bg-[#c2dbc4] text-[#222222] p-6 rounded-lg shadow-md mb-8">
          <div className="mb-4">
            <label className="block mb-2 font-semibold">Lataa tiliote CSV muodossa</label>
            <input
              type="file"
              accept=".csv"
              onChange={handleFileUpload}
              className="w-full border p-2 rounded bg-white"
            />
          </div>

          <button
            onClick={analyzeFile}
            disabled={loading || !file}
            className="w-full bg-[#222222] text-[#c2dbc4] py-3 rounded font-bold disabled:opacity-50"
          >
            {loading ? 'Analysoidaan' : 'Analysoi tiliote'}
          </button>
        </div>

        {data && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div className="bg-[#c2dbc4] text-[#222222] p-6 rounded-lg shadow-md">
              <h2 className="text-2xl font-bold mb-4">Yhteenveto</h2>
              <div className="space-y-2">
                {data.summary.map((item, index) => (
                  <div key={index} className="flex justify-between border-b border-[#222222] pb-2">
                    <span className="font-semibold">{item.category}</span>
                    <span>{item.total} €</span>
                  </div>
                ))}
              </div>
            </div>

            <div className="bg-[#c2dbc4] text-[#222222] p-6 rounded-lg shadow-md">
              <h2 className="text-2xl font-bold mb-4">Tapahtumat</h2>
              <div className="space-y-4">
                {data.transactions.map((transaction, index) => (
                  <div key={index} className="border-l-4 border-[#222222] pl-4">
                    <div className="flex justify-between font-bold">
                      <span>{transaction.description}</span>
                      <span>{transaction.amount} €</span>
                    </div>
                    <div className="flex justify-between text-sm mt-1">
                      <span>{transaction.date}</span>
                      <span className="bg-[#222222] text-[#c2dbc4] px-2 py-1 rounded text-xs">
                        {transaction.category}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
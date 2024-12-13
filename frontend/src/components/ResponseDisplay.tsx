
interface ResponseDisplayProps {
  response: string;
}

export const ResponseDisplay = ({ response }: ResponseDisplayProps) => (
  <div className="p-4 border rounded-md bg-gray-100">
    {response ? (
      <p className="text-gray-700">{response}</p>
    ) : (
      <p className="text-gray-500 italic">Waiting for your message...</p>
    )}
  </div>
);

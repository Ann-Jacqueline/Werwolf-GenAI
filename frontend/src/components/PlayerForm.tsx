import React from 'react';

interface PlayerFormProps {
  playerCount: number;
  onPlayerCountChange: (count: number) => void;
  onSubmit: (e: React.FormEvent) => void;
  userInput: string;
  onUserInputChange: (input: string) => void;
  isLoading?: boolean;
}

export const PlayerForm = ({
  playerCount,
  onPlayerCountChange,
  onSubmit,
  userInput,
  onUserInputChange,
  isLoading = false
}: PlayerFormProps) => (
  <form onSubmit={onSubmit} className="space-y-4">
    <div>
      <label htmlFor="players" className="block text-sm font-medium text-gray-700 mb-1">
        Number of Players
      </label>
      <input
        type="number"
        id="players"
        min="7"
        max="20"
        value={playerCount}
        onChange={(e) => onPlayerCountChange(parseInt(e.target.value) || 1)}
        className="input-animated w-full pl-4 pr-4 py-3 rounded-lg border border-gray-300 shadow focus:outline-none"
      />
    </div>
    <div>
      <label htmlFor="message" className="block text-sm font-medium text-gray-700 mb-1">
        Your Message
      </label>
      <textarea
        id="message"
        rows={3}
        value={userInput}
        onChange={(e) => onUserInputChange(e.target.value)}
        className="input-animated w-full pl-4 pr-4 py-3 rounded-lg border border-gray-300 shadow focus:outline-none"
        placeholder="Type your message here..."
      />
    </div>
    <button
      type="submit"
      disabled={isLoading}
      className="w-full bg-blue-500 text-white p-2 rounded-md hover:bg-blue-600 disabled:bg-gray-300"
    >
      {isLoading ? 'Sending...' : 'Send Message'}
    </button>
  </form>
);
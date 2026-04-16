import React from "react";

function BaseModal({ children }: { children: React.ReactNode }) {
	return (
		<div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
			<div className="flex flex-col bg-white p-6 shadow-md shadow-black rounded-lg w-96 h-96">
				{children}
			</div>
		</div>
	);
}

export default BaseModal;

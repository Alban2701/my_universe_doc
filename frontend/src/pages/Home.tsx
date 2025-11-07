import Header from "../components/Header";
import RectangularButton from "../components/Button/rectangular.button";

export default function Home() {
	return (
		<div className="min-h-screen flex flex-col bg-gray-50 text-gray-900">
			{/* --- HEADER --- */}
			<Header />

			{/* --- HERO SECTION --- */}
			<section className="flex flex-col justify-center items-center text-center mt-24 px-6">
				<h1 className="text-5xl font-bold mb-4 text-gray-900">
					My Universe Doc
				</h1>
				<p className="text-lg text-gray-600 max-w-2xl mb-8">
					Documentez, explorez et partagez vos univers narratifs. Une plateforme
					moderne pour les créateurs, les rôlistes et les écrivains du futur.
				</p>
				<div className="flex gap-4">
					<RectangularButton
						url="/"
						text="Créez un compte pour découvrir maintenant !"
						color="blue"
					/>
					<button
						type="button"
						className="border border-blue-600 text-blue-600 font-medium px-6 py-3 rounded-lg hover:bg-blue-50 transition"
					>
						En savoir plus
					</button>
				</div>
			</section>

			{/* --- FEATURES --- */}
			<section className="mt-24 px-6">
				<h2 className="text-3xl font-semibold text-center mb-10">
					Fonctionnalités principales
				</h2>
				<div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
					{/* Feature 1 */}
					<div className="bg-white rounded-2xl shadow p-6 flex flex-col items-center text-center">
						<img
							src="/icons/document.svg"
							alt="Documentation"
							className="w-16 h-16 mb-4"
						/>
						<h3 className="text-xl font-semibold mb-2">
							Documentation centralisée
						</h3>
						<p className="text-gray-600">
							Organisez vos mondes, personnages et lieux en un seul endroit.
						</p>
					</div>

					{/* Feature 2 */}
					<div className="bg-white rounded-2xl shadow p-6 flex flex-col items-center text-center">
						<img
							src="/icons/shield.svg"
							alt="Accès sécurisé"
							className="w-16 h-16 mb-4"
						/>
						<h3 className="text-xl font-semibold mb-2">Contrôle des accès</h3>
						<p className="text-gray-600">
							Gérez qui peut consulter ou modifier vos univers.
						</p>
					</div>

					{/* Feature 3 */}
					<div className="bg-white rounded-2xl shadow p-6 flex flex-col items-center text-center">
						<img
							src="/icons/collab.svg"
							alt="Collaboration"
							className="w-16 h-16 mb-4"
						/>
						<h3 className="text-xl font-semibold mb-2">
							Collaboration avec suivi et validation des changements
						</h3>
						<p className="text-gray-600">
							Travaillez avec vos amis ou votre équipe sans perdre la cohérence
							de l'univers.
						</p>
					</div>
				</div>
			</section>

			{/* --- ABOUT --- */}
			<section className="mt-24 bg-gray-100 py-16 px-6">
				<div className="max-w-4xl mx-auto text-center">
					<h2 className="text-3xl font-semibold mb-6">
						Pourquoi My Universe Doc ?
					</h2>
					<p className="text-gray-700 leading-relaxed">
						My Universe Doc est né d'un besoin simple : permettre aux créateurs
						d'univers de garder une trace claire et structurée de leur travail.
						Fini les fichiers dispersés et les notes introuvables — tout est
						organisé, connecté et accessible depuis une interface fluide.
					</p>
				</div>
			</section>

			{/* --- FOOTER --- */}
			<footer className="mt-auto bg-gray-900 text-gray-300 text-center py-6">
				<p>
					© {new Date().getFullYear()} My Universe Doc — Tous droits réservés.
				</p>
			</footer>
		</div>
	);
}

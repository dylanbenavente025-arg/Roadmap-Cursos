import CatalogoPage from '../features/catalogo/components/CatalogoPage.jsx'

export default function App() {
  return (
    <>
      <header className="header">
        <div className="contenedor header__contenido">
          <span className="header__logo">AprovechaElBug</span>
        </div>
      </header>
      <main className="contenedor">
        <CatalogoPage />
      </main>
    </>
  )
}
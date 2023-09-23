import Footer from "./Footer"
import Main from "./Main"
import Navbar from "./Navbar"

function Home() {
  return (
    <div>
        {/* <nav className="p-5 flex justify-evenly bg-white dark:bg-gray-900 text-gray-900 uppercase dark:text-white"> 
            <span>Home</span>
            <span>About us</span>
            <span>Start speaking!</span>
        </nav> */}
        <div>
            <Navbar />
        </div>
        <div className="">
            <Main />
        </div>
        <div>
            <Footer />
        </div>
    </div>
  )
}

export default Home
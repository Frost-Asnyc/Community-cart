
import { Leaf } from "lucide-react";

import Hero from "../components/Hero";
import Manifesto from "../components/Manifesto";
import SellStrip from "../components/SellStrip";

/*
  DEVELOPER: Vincent

  RESPONSIBILITY:
  Compose the LocalLoop homepage.

  NOTES:
  - Marketplace listings will be connected to the backend later.
  - No demo or external placeholder listings are displayed.
  - App.jsx handles authentication and navigation.
*/

function Home({ onShowAllFinds, onCreateListing }) {
  return (
    <main>
      <Hero onShowAllFinds={onShowAllFinds} />

      <div
        className="loop-ticker"
        aria-label="LocalLoop community highlights"
      >
        <div className="loop-ticker-track">
          <span>GOODS WITH STORIES</span>
          <Leaf size={13} />
          <span>BUY NEARBY</span>
          <Leaf size={13} />
          <span>LOVE IT LONGER</span>
          <Leaf size={13} />
          <span>PASS IT FORWARD</span>
          <Leaf size={13} />

          <span aria-hidden="true">GOODS WITH STORIES</span>
          <Leaf size={13} aria-hidden="true" />
          <span aria-hidden="true">BUY NEARBY</span>
          <Leaf size={13} aria-hidden="true" />
          <span aria-hidden="true">LOVE IT LONGER</span>
          <Leaf size={13} aria-hidden="true" />
          <span aria-hidden="true">PASS IT FORWARD</span>
          <Leaf size={13} aria-hidden="true" />
        </div>
      </div>

      {/* Backend marketplace listings will be integrated here. */}
      <section
        className="finds-section"
        id="finds"
        aria-labelledby="finds-title"
        data-reveal
      >
        <div className="section-heading">
          <div>
            <div className="eyebrow">
              <span className="eyebrow-dot" /> AROUND THE CORNER
            </div>

            <h2 id="finds-title">A few good finds.</h2>

            <p>
              One person's maybe is another person's absolutely.
            </p>
          </div>
        </div>
      </section>

      <Manifesto onShowAllFinds={onShowAllFinds} />

      <SellStrip onCreateListing={onCreateListing} />
    </main>
  );
}

export default Home;

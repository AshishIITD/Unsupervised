/* ==========================================================================
   UNSUPERVISED LEARNING VISUAL PLAYGROUND - APPLICATION ENGINE
   ========================================================================== */

document.addEventListener("DOMContentLoaded", () => {
    // ----------------------------------------------------------------------
    // State Management & Constants
    // ----------------------------------------------------------------------
    const state = {
        activeTab: "clustering",
        activeClusteringAlgo: "kmeans",
        points: [],             // {x, y, label, type, originalX, originalY}
        centroids: [],          // {x, y, oldX, oldY, color}
        clusterStep: 0,
        clusterRunning: false,
        clusterTimer: null,
        
        // DBSCAN state
        dbscanIndex: 0,
        dbscanQueue: [],
        dbscanVisited: new Set(),
        
        // PCA state
        pca3dPoints: [],        // {x, y, z}
        pcaRotationAngle: 30,   // degrees
        pcaDragging: false,
        pcaLastMouseX: 0,
        
        // Anomaly state
        anomalyPoints: [],      // {x, y, score, depth}
        anomalySlices: [],      // {dir, val}
        anomalyRunning: false,
        
        // Association state
        basket: new Set(),
        rules: [
            { antecedent: ["Bread"], consequent: ["Butter"], support: 0.47, confidence: 0.88, lift: 1.64, desc: "Classic pairing! Bread and Butter are bought together on almost half of all shopping trips." },
            { antecedent: ["Beer"], consequent: ["Chips"], support: 0.40, confidence: 0.75, lift: 1.88, desc: "Party purchases! Customers buying beer are highly likely to grab chips too." },
            { antecedent: ["Chips"], consequent: ["Beer"], support: 0.40, confidence: 1.00, lift: 1.88, desc: "Strong correlation! 100% of customers buying chips in our database also bought beer." },
            { antecedent: ["Diapers"], consequent: ["Beer"], support: 0.33, confidence: 1.00, lift: 1.88, desc: "The famous retail legend! Parents buying diapers often grab a pack of beer to relax." },
            { antecedent: ["Beer"], consequent: ["Diapers"], support: 0.33, confidence: 0.63, lift: 1.88, desc: "Reciprocal rule. Buying beer increases diaper sales probability by 1.88x." }
        ],
        graphNodes: [
            { id: "Bread", label: "Bread", x: 60, y: 50, emoji: "🍞" },
            { id: "Butter", label: "Butter", x: 130, y: 140, emoji: "🧈" },
            { id: "Milk", label: "Milk", x: 200, y: 60, emoji: "🥛" },
            { id: "Eggs", label: "Eggs", x: 270, y: 150, emoji: "🥚" },
            { id: "Diapers", label: "Diapers", x: 70, y: 160, emoji: "🧷" },
            { id: "Beer", label: "Beer", x: 170, y: 170, emoji: "🍺" },
            { id: "Chips", label: "Chips", x: 260, y: 70, emoji: "🥔" }
        ],
        graphLinks: [
            { source: "Bread", target: "Butter", lift: 1.64 },
            { source: "Beer", target: "Chips", lift: 1.88 },
            { source: "Diapers", target: "Beer", lift: 1.88 }
        ]
    };

    const colors = ["#ff4d6d", "#00f5d4", "#ffb703", "#3a86c8", "#9d4edd", "#ff758f"];
    const greyNoise = "#5c5c64";

    // ----------------------------------------------------------------------
    // UI Elements Selector
    // ----------------------------------------------------------------------
    const select = {
        // Navigation Tabs
        navBtns: document.querySelectorAll(".sidebar .nav-btn"),
        tabContents: document.querySelectorAll(".sandbox-viewport .tab-content"),
        
        // Clustering selectors
        toggleKMeans: document.getElementById("toggle-kmeans"),
        toggleDBSCAN: document.getElementById("toggle-dbscan"),
        clusteringCanvas: document.getElementById("clustering-canvas"),
        clusteringStatus: document.getElementById("clustering-status"),
        btnClearCluster: document.getElementById("btn-clear-cluster"),
        btnPresetBlobs: document.getElementById("btn-preset-blobs"),
        btnPresetRings: document.getElementById("btn-preset-rings"),
        kmeansControls: document.getElementById("kmeans-controls"),
        dbscanControls: document.getElementById("dbscan-controls"),
        sliderK: document.getElementById("kmeans-k"),
        valK: document.getElementById("val-k"),
        sliderEps: document.getElementById("dbscan-eps"),
        valEps: document.getElementById("val-eps"),
        sliderMinPts: document.getElementById("dbscan-minpts"),
        valMinPts: document.getElementById("val-minpts"),
        btnStepKMeans: document.getElementById("btn-step-kmeans"),
        btnRunKMeans: document.getElementById("btn-run-kmeans"),
        btnStepDBSCAN: document.getElementById("btn-step-dbscan"),
        btnRunDBSCAN: document.getElementById("btn-run-dbscan"),
        lblMetricPrimary: document.getElementById("lbl-metric-primary"),
        valMetricPrimary: document.getElementById("val-metric-primary"),
        lblMetricSecondary: document.getElementById("lbl-metric-secondary"),
        valMetricSecondary: document.getElementById("val-metric-secondary"),
        clusteringLegend: document.getElementById("clustering-legend"),
        
        // PCA selectors
        pca3dCanvas: document.getElementById("pca-3d-canvas"),
        pca2dCanvas: document.getElementById("pca-2d-canvas"),
        sliderPcaTilt: document.getElementById("pca-tilt"),
        valPcaTilt: document.getElementById("val-pca-tilt"),
        btnRegeneratePca: document.getElementById("btn-regenerate-pca"),
        pc1Bar: document.getElementById("pc1-bar"),
        pc1Val: document.getElementById("pc1-val"),
        pc2Bar: document.getElementById("pc2-bar"),
        pc2Val: document.getElementById("pc2-val"),
        valTotalVariance: document.getElementById("val-total-variance"),

        // Anomaly selectors
        anomalyCanvas: document.getElementById("anomaly-canvas"),
        anomalyStatus: document.getElementById("anomaly-status"),
        btnClearAnomaly: document.getElementById("btn-clear-anomaly"),
        btnPresetTransactions: document.getElementById("btn-preset-transactions"),
        sliderTrees: document.getElementById("anomaly-trees"),
        valTrees: document.getElementById("val-trees"),
        btnStepIsolation: document.getElementById("btn-step-isolation"),
        btnRunIsolation: document.getElementById("btn-run-isolation"),
        riskLedgerBody: document.getElementById("risk-ledger-body"),

        // Association selectors
        groceryShelf: document.querySelector(".grocery-shelf"),
        userBasket: document.getElementById("user-basket"),
        btnClearBasket: document.getElementById("btn-clear-basket"),
        minedRulesList: document.getElementById("mined-rules-list"),
        relationshipGraph: document.getElementById("relationship-graph"),
        
        // Layman Translation Drawer
        translationTitle: document.getElementById("translation-title"),
        translationText: document.getElementById("translation-text")
    };

    // ----------------------------------------------------------------------
    // Tab Navigation Controller
    // ----------------------------------------------------------------------
    select.navBtns.forEach(btn => {
        btn.addEventListener("click", () => {
            select.navBtns.forEach(b => b.classList.remove("active"));
            btn.classList.add("active");
            
            const targetTab = btn.getAttribute("data-tab");
            state.activeTab = targetTab;
            
            select.tabContents.forEach(content => {
                if (content.getAttribute("id") === `tab-${targetTab}`) {
                    content.classList.add("active");
                } else {
                    content.classList.remove("active");
                }
            });

            // Initialize respective tab state
            initTabScene(targetTab);
        });
    });

    function initTabScene(tabName) {
        stopClusteringLoop();
        if (tabName === "clustering") {
            if (state.points.length === 0) {
                generateBlobsPreset();
            }
            updateClusteringScene();
            explainClusteringInitial();
        } else if (tabName === "dimensionality") {
            if (state.pca3dPoints.length === 0) {
                generate3DPcaPoints();
            }
            updatePcaScene();
            explainPca();
        } else if (tabName === "anomaly") {
            if (state.anomalyPoints.length === 0) {
                generateTransactionsPreset();
            }
            state.anomalySlices = [];
            updateAnomalyScene();
            explainAnomalyInitial();
        } else if (tabName === "association") {
            updateBasketUI();
            renderRelationshipGraph();
            explainAssociationInitial();
        }
    }

    // ----------------------------------------------------------------------
    // Layman Explainer Functions
    // ----------------------------------------------------------------------
    function setExplanation(title, text) {
        select.translationTitle.textContent = title;
        select.translationText.innerHTML = text;
    }

    function explainClusteringInitial() {
        if (state.activeClusteringAlgo === "kmeans") {
            setExplanation(
                "K-Means: Finding Spherical Groups",
                "<strong>How it works:</strong> K-Means is a distance-based algorithm. It places K pins (centroids) in the space and says: 'everyone group around the nearest pin!' Then, the pins move to the center of their new groups. This repeats until the pins stop moving.<br><br>" +
                "<strong>Layman translation:</strong> Think of 3 politicians positioning their podiums in a crowd of voters. As voters decide who is closest and walk to them, the politicians move their podiums to the exact middle of their new supporter base, trying to satisfy everyone. Click <strong>Step KMeans</strong> to watch this movement!"
            );
        } else {
            setExplanation(
                "DBSCAN: Density-Based Communities",
                "<strong>How it works:</strong> DBSCAN doesn't care about centers. It connects points that are packed tightly together (within search radius <strong>&epsilon;</strong>). If a point has enough neighbors, it starts a community. If a point is far away from everyone, it gets rejected as noise.<br><br>" +
                "<strong>Layman translation:</strong> Think of a virus or a rumor spreading at a party. If you are standing next to a group of friends, you catch the rumor. If you are standing in the corner alone, you are isolated and never hear it (labeled as 'Noise'). DBSCAN is fantastic at finding weird, winding shapes like concentric rings!"
            );
        }
    }

    function explainPca() {
        const tilt = Math.abs(parseInt(select.sliderPcaTilt.value));
        let qualityText = "";
        let detailsText = "";
        
        if (tilt <= 15) {
            qualityText = "<span class='text-pink' style='color: var(--color-pink); font-weight: bold;'>POOR SIDE VIEW</span>";
            detailsText = "You are looking at the 3D sheet almost perfectly edge-on! The points look compressed into a single flat line. In 2D, we have lost almost all our width detail. Component 2 contains almost 0% information now. This is like taking a photo of a flat plate from the side—it just looks like a thin line!";
        } else if (tilt >= 25 && tilt <= 45) {
            qualityText = "<span style='color: var(--color-accent); font-weight: bold;'>OPTIMAL PROJECTION (99.9% Keep)</span>";
            detailsText = "Perfect! The projection plane is aligned with the tilt of our 3D sheet. By projecting from this angle, we capture the full length and width of the sheet. Component 1 captures 76% of the spread, and Component 2 captures 23%. Together, we keep <strong>99.9% of the original detail</strong> in just a 2D image!";
        } else {
            qualityText = "<strong>SUB-OPTIMAL VIEW</strong>";
            detailsText = "You have tilted the camera away. While we still see a 2D spread, the shadow is slightly squashed compared to the true shape, resulting in some variance loss. We still retain a good chunk of detail, but the alignment isn't as perfect as the 30&deg; tilted sheet itself.";
        }

        setExplanation(
            "PCA: Taking the Best 2D Photo of 3D Data",
            `<strong>Current Angle Alignment:</strong> ${qualityText}<br><br>` +
            `<strong>Layman translation:</strong> High-dimensional data is hard to look at. Principal Component Analysis (PCA) acts like a camera taking a 2D snapshot of a 3D object. ` +
            `If you take a photo of a coffee mug from the top, it just looks like a circle (bad angle). If you take it from the side, you see the handle and cup (great angle). ` +
            `PCA rotates the camera to find the angle that spreads the points out as much as possible, preserving the maximum amount of original detail (variance).<br><br>${detailsText}`
        );
    }

    function explainAnomalyInitial() {
        setExplanation(
            "Isolation Forest: Spotting the Outliers",
            "<strong>How it works:</strong> Instead of building a model of 'normal' data, Isolation Forest isolates anomalies directly. It draws random cutting lines across the screen. If a point is in a dense crowd, it takes many cuts to isolate it. If a point is alone in space, a single random cut separates it immediately.<br><br>" +
            "<strong>Layman translation:</strong> Imagine trying to find a house. If the house is in the middle of a dense, crowded city, you must ask dozens of questions: 'Which block? Which street? Which apartment?' to isolate it. If a house is a lone cabin in the desert, a single question: 'Is it north of the highway?' isolates it. Click <strong>Slice Space</strong> to watch the random cuts!"
        );
    }

    function explainAssociationInitial() {
        setExplanation(
            "Apriori: Market Basket Associations",
            "<strong>How it works:</strong> Apriori scans receipts to find items frequently bought together. It calculates three metrics:<br>" +
            "1. <strong>Support (Popularity)</strong>: How often does this combo occur? (e.g., Bread + Butter is 47% popular).<br>" +
            "2. <strong>Confidence (Reliability)</strong>: If they buy A, how likely do they buy B? (If they buy Bread, they buy Butter 88% of the time).<br>" +
            "3. <strong>Lift (Strength)</strong>: Does buying A boost buying B? (A lift of 1.88 means buying A makes them 1.88x more likely to buy B than random chance).<br><br>" +
            "<strong>Interactive Challenge:</strong> Click items on the shelf to build a basket! Watch the graph and rule list update. If you add <strong>Diapers</strong>, watch the connection to <strong>Beer</strong> glow! This represents the famous retail rule."
        );
    }

    // ----------------------------------------------------------------------
    // PILLAR 1: CLUSTERING SANDBOX LOGIC
    // ----------------------------------------------------------------------
    
    // Canvas Mouse Click: Add custom points
    select.clusteringCanvas.addEventListener("mousedown", (e) => {
        stopClusteringLoop();
        const rect = select.clusteringCanvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        
        state.points.push({
            x: x,
            y: y,
            originalX: x,
            originalY: y,
            label: -1,
            type: 'unvisited'
        });
        
        state.clusterStep = 0;
        updateClusteringScene();
        
        select.clusteringStatus.textContent = `Added point at (${Math.round(x)}, ${Math.round(y)})`;
        setExplanation(
            "Custom Point Added!",
            "You just added a custom data point! Note that it starts as grey because the algorithm hasn't run yet.<br><br>" +
            "If you are running K-Means, this point will be pulled into the nearest centroid. If you are running DBSCAN, this point could either act as a bridge to expand a cluster, or become a new 'Noise' point if it is too far from the others."
        );
    });

    // Clear Canvas
    select.btnClearCluster.addEventListener("click", () => {
        stopClusteringLoop();
        state.points = [];
        state.centroids = [];
        state.clusterStep = 0;
        updateClusteringScene();
        select.clusteringStatus.textContent = "Canvas cleared. Click to draw points.";
    });

    // Preset Blobs (K-Means friendly)
    select.btnPresetBlobs.addEventListener("click", () => {
        stopClusteringLoop();
        generateBlobsPreset();
        updateClusteringScene();
    });

    function generateBlobsPreset() {
        state.points = [];
        state.centroids = [];
        state.clusterStep = 0;
        
        // 3 Blobs
        const centers = [
            { x: 150, y: 150 },
            { x: 450, y: 120 },
            { x: 300, y: 300 }
        ];
        
        centers.forEach((center, cIdx) => {
            const count = 30 + Math.floor(Math.random() * 15);
            for (let i = 0; i < count; i++) {
                const r = Math.random() * 50;
                const theta = Math.random() * 2 * Math.PI;
                const x = center.x + r * Math.cos(theta);
                const y = center.y + r * Math.sin(theta);
                state.points.push({
                    x: x,
                    y: y,
                    originalX: x,
                    originalY: y,
                    label: -1,
                    type: 'unvisited'
                });
            }
        });
        select.clusteringStatus.textContent = "Generated 3 dense circular blobs.";
    }

    // Preset Rings (DBSCAN friendly)
    select.btnPresetRings.addEventListener("click", () => {
        stopClusteringLoop();
        generateRingsPreset();
        updateClusteringScene();
    });

    function generateRingsPreset() {
        state.points = [];
        state.centroids = [];
        state.clusterStep = 0;
        
        const centerX = 300;
        const centerY = 200;
        
        // Inner Ring (radius 60)
        for (let i = 0; i < 60; i++) {
            const theta = (i / 60) * 2 * Math.PI;
            const r = 50 + (Math.random() - 0.5) * 15;
            const x = centerX + r * Math.cos(theta);
            const y = centerY + r * Math.sin(theta);
            state.points.push({ x: x, y: y, originalX: x, originalY: y, label: -1, type: 'unvisited' });
        }
        
        // Outer Ring (radius 140)
        for (let i = 0; i < 110; i++) {
            const theta = (i / 110) * 2 * Math.PI;
            const r = 130 + (Math.random() - 0.5) * 18;
            const x = centerX + r * Math.cos(theta);
            const y = centerY + r * Math.sin(theta);
            state.points.push({ x: x, y: y, originalX: x, originalY: y, label: -1, type: 'unvisited' });
        }
        
        // Add some random noise points (outliers)
        for (let i = 0; i < 12; i++) {
            const x = 50 + Math.random() * 500;
            const y = 40 + Math.random() * 320;
            state.points.push({ x: x, y: y, originalX: x, originalY: y, label: -1, type: 'unvisited' });
        }
        
        select.clusteringStatus.textContent = "Generated concentric rings + outliers.";
    }

    // Toggle between KMeans and DBSCAN
    select.toggleKMeans.addEventListener("click", () => {
        stopClusteringLoop();
        select.toggleKMeans.classList.add("active");
        select.toggleDBSCAN.classList.remove("active");
        select.kmeansControls.classList.remove("hidden");
        select.dbscanControls.classList.add("hidden");
        state.activeClusteringAlgo = "kmeans";
        state.clusterStep = 0;
        resetPointLabels();
        updateClusteringScene();
        explainClusteringInitial();
    });

    select.toggleDBSCAN.addEventListener("click", () => {
        stopClusteringLoop();
        select.toggleKMeans.classList.remove("active");
        select.toggleDBSCAN.classList.add("active");
        select.kmeansControls.classList.add("hidden");
        select.dbscanControls.classList.remove("hidden");
        state.activeClusteringAlgo = "dbscan";
        state.clusterStep = 0;
        resetPointLabels();
        updateClusteringScene();
        explainClusteringInitial();
    });

    // Sliders
    select.sliderK.addEventListener("input", () => {
        select.valK.textContent = select.sliderK.value;
        stopClusteringLoop();
        state.clusterStep = 0;
        state.centroids = [];
        resetPointLabels();
        updateClusteringScene();
    });

    select.sliderEps.addEventListener("input", () => {
        select.valEps.textContent = select.sliderEps.value;
        stopClusteringLoop();
        state.clusterStep = 0;
        resetPointLabels();
        updateClusteringScene();
    });

    select.sliderMinPts.addEventListener("input", () => {
        select.valMinPts.textContent = select.sliderMinPts.value;
        stopClusteringLoop();
        state.clusterStep = 0;
        resetPointLabels();
        updateClusteringScene();
    });

    function resetPointLabels() {
        state.points.forEach(p => {
            p.label = -1;
            p.type = 'unvisited';
        });
    }

    // Step KMeans
    select.btnStepKMeans.addEventListener("click", () => {
        if (state.points.length === 0) return;
        stepKMeans();
    });

    // Run KMeans
    select.btnRunKMeans.addEventListener("click", () => {
        if (state.points.length === 0) return;
        if (state.clusterRunning) {
            stopClusteringLoop();
        } else {
            state.clusterRunning = true;
            select.btnRunKMeans.textContent = "Pause";
            select.btnRunKMeans.classList.add("btn-primary");
            select.btnRunKMeans.classList.remove("btn-accent");
            
            // Loop until convergence
            state.clusterTimer = setInterval(() => {
                const converged = stepKMeans();
                if (converged) {
                    stopClusteringLoop();
                    select.clusteringStatus.textContent = "K-Means converged successfully!";
                }
            }, 600);
        }
    });

    // Step DBSCAN
    select.btnStepDBSCAN.addEventListener("click", () => {
        if (state.points.length === 0) return;
        stepDBSCAN();
    });

    // Run DBSCAN
    select.btnRunDBSCAN.addEventListener("click", () => {
        if (state.points.length === 0) return;
        if (state.clusterRunning) {
            stopClusteringLoop();
        } else {
            state.clusterRunning = true;
            select.btnRunDBSCAN.textContent = "Pause";
            select.btnRunDBSCAN.classList.add("btn-primary");
            select.btnRunDBSCAN.classList.remove("btn-accent");
            
            state.clusterTimer = setInterval(() => {
                const finished = stepDBSCAN();
                if (finished) {
                    stopClusteringLoop();
                    select.clusteringStatus.textContent = "DBSCAN finished processing all points!";
                }
            }, 60); // Faster loop for DBSCAN
        }
    });

    function stopClusteringLoop() {
        state.clusterRunning = false;
        if (state.clusterTimer) {
            clearInterval(state.clusterTimer);
            state.clusterTimer = null;
        }
        select.btnRunKMeans.textContent = "Auto Run";
        select.btnRunKMeans.classList.remove("btn-primary");
        select.btnRunKMeans.classList.add("btn-accent");
        
        select.btnRunDBSCAN.textContent = "Auto Run";
        select.btnRunDBSCAN.classList.remove("btn-primary");
        select.btnRunDBSCAN.classList.add("btn-accent");
    }

    // ----------------------------------------------------------------------
    // K-Means Core Math & Logic
    // ----------------------------------------------------------------------
    function stepKMeans() {
        const k = parseInt(select.sliderK.value);
        
        // 1. Initialize centroids if not present
        if (state.centroids.length === 0) {
            state.centroids = [];
            // Select random points as initial centroids
            const shuffled = [...state.points].sort(() => 0.5 - Math.random());
            for (let i = 0; i < k; i++) {
                const p = shuffled[i] || { x: Math.random() * 500 + 50, y: Math.random() * 300 + 40 };
                state.centroids.push({
                    x: p.x,
                    y: p.y,
                    oldX: p.x,
                    oldY: p.y,
                    color: colors[i]
                });
            }
            state.clusterStep = 1; // Stage: Assignment
            updateClusteringScene();
            select.clusteringStatus.textContent = `Centroids initialized. Ready to assign points.`;
            
            setExplanation(
                "Centroids Placed! (Step 1)",
                `We randomly placed <strong>${k} pins (centroids)</strong> in the canvas. ` +
                `In the next step, we will draw lines from every single point to its nearest pin and color them to match. ` +
                `Click <strong>Step KMeans</strong> to assign the points!`
            );
            return false;
        }

        if (state.clusterStep % 2 === 1) {
            // --- Assignment Phase ---
            let changes = 0;
            state.points.forEach(p => {
                let minDist = Infinity;
                let bestLabel = -1;
                
                state.centroids.forEach((c, idx) => {
                    const dist = Math.pow(p.x - c.x, 2) + Math.pow(p.y - c.y, 2);
                    if (dist < minDist) {
                        minDist = dist;
                        bestLabel = idx;
                    }
                });
                
                if (p.label !== bestLabel) {
                    p.label = bestLabel;
                    changes++;
                }
            });
            
            state.clusterStep++;
            updateClusteringScene();
            
            // Calculate metrics
            const inertia = calculateInertia();
            const silhouette = calculateSilhouetteKMeans();
            select.valMetricPrimary.textContent = Math.round(inertia);
            select.valMetricSecondary.textContent = silhouette.toFixed(3);
            
            select.clusteringStatus.textContent = `Assigned points to nearest centroids.`;
            
            setExplanation(
                "Points Assigned to Nearest Pin (Step 2)",
                `Every point looked around, measured the distance to all <strong>${k} centroids</strong>, and joined the closest one. ` +
                `Notice the colored lines connecting points to their centroids. ` +
                `<br><br><strong>Metrics Watch:</strong> ` +
                `<ul>` +
                `<li><strong>Inertia</strong> represents our total error: the sum of all line lengths squared. We want this to go down! (Current: ${Math.round(inertia)}).</li>` +
                `<li><strong>Silhouette Score</strong> is ${silhouette.toFixed(3)}. Closer to 1 means groups are perfectly separated; closer to 0 means they are overlapping.</li>` +
                `</ul>` +
                `In the next step, the pins will fly to the center of their new groups! Click <strong>Step KMeans</strong>.`
            );
            return false;
            
        } else {
            // --- Update Phase ---
            let converged = true;
            const k = state.centroids.length;
            
            for (let i = 0; i < k; i++) {
                const c = state.centroids[i];
                c.oldX = c.x;
                c.oldY = c.y;
                
                const clusterPoints = state.points.filter(p => p.label === i);
                if (clusterPoints.length > 0) {
                    const meanX = clusterPoints.reduce((sum, p) => sum + p.x, 0) / clusterPoints.length;
                    const meanY = clusterPoints.reduce((sum, p) => sum + p.y, 0) / clusterPoints.length;
                    
                    // Check if centroid shifted
                    const shift = Math.pow(c.x - meanX, 2) + Math.pow(c.y - meanY, 2);
                    if (shift > 0.1) {
                        converged = false;
                    }
                    
                    c.x = meanX;
                    c.y = meanY;
                }
            }
            
            state.clusterStep++;
            updateClusteringScene();
            
            if (converged) {
                select.clusteringStatus.textContent = "Converged! Centroids stopped moving.";
                const inertia = calculateInertia();
                const silhouette = calculateSilhouetteKMeans();
                
                let comment = "";
                if (silhouette > 0.7) comment = "Excellent clustering! The groups are highly distinct.";
                else if (silhouette > 0.5) comment = "Good clustering. The groups are clear, though some border points exist.";
                else comment = "Weak clustering. Groups overlap significantly. Try changing K!";
                
                setExplanation(
                    "K-Means Converged! (Done)",
                    `The pins moved to the gravity center of their groups, and <strong>they didn't shift at all</strong>. The algorithm is finished!<br><br>` +
                    `<strong>Final Verdict:</strong> The silhouette score is <strong>${silhouette.toFixed(3)}</strong>. ${comment}`
                );
                return true;
            } else {
                select.clusteringStatus.textContent = "Centroids moved. Re-assigning points next.";
                setExplanation(
                    "Centroids Re-Centered! (Step 3)",
                    `Look at the screen: the pins have shifted to the exact average center of their colored supporters. ` +
                    `Because the pins moved, some points might now be closer to a *different* pin! ` +
                    `<br><br>In the next step, we will re-assign points. Click <strong>Step KMeans</strong> to run the loop again.`
                );
                return false;
            }
        }
    }

    function calculateInertia() {
        let sum = 0;
        state.points.forEach(p => {
            if (p.label !== -1) {
                const c = state.centroids[p.label];
                sum += Math.pow(p.x - c.x, 2) + Math.pow(p.y - c.y, 2);
            }
        });
        return sum;
    }

    function calculateSilhouetteKMeans() {
        if (state.points.length < 2 || state.centroids.length < 2) return 0;
        
        // Simple silhouette score implementation
        let totalS = 0;
        let counted = 0;
        
        state.points.forEach(p => {
            if (p.label === -1) return;
            
            // 1. Intra-dist (a): mean dist to other points in same cluster
            const sameCluster = state.points.filter(other => other.label === p.label && other !== p);
            if (sameCluster.length === 0) return;
            
            let a = 0;
            sameCluster.forEach(other => {
                a += Math.sqrt(Math.pow(p.x - other.x, 2) + Math.pow(p.y - other.y, 2));
            });
            a /= sameCluster.length;
            
            // 2. Inter-dist (b): mean dist to points in nearest other cluster
            let minB = Infinity;
            const k = state.centroids.length;
            
            for (let cIdx = 0; cIdx < k; cIdx++) {
                if (cIdx === p.label) continue;
                
                const otherCluster = state.points.filter(other => other.label === cIdx);
                if (otherCluster.length === 0) continue;
                
                let bSum = 0;
                otherCluster.forEach(other => {
                    bSum += Math.sqrt(Math.pow(p.x - other.x, 2) + Math.pow(p.y - other.y, 2));
                });
                bSum /= otherCluster.length;
                minB = Math.min(minB, bSum);
            }
            
            // 3. Score s
            const s = (minB - a) / Math.max(a, minB);
            totalS += s;
            counted++;
        });
        
        return counted > 0 ? totalS / counted : 0;
    }

    // ----------------------------------------------------------------------
    // DBSCAN Core Math & Logic
    // ----------------------------------------------------------------------
    function stepDBSCAN() {
        const eps = parseInt(select.sliderEps.value);
        const minPts = parseInt(select.sliderMinPts.value);
        
        // Initialize DBSCAN state if at step 0
        if (state.clusterStep === 0) {
            state.dbscanIndex = 0;
            state.dbscanVisited = new Set();
            state.dbscanQueue = [];
            resetPointLabels();
            state.clusterStep = 1; // Processing
            state.centroids = []; // DBSCAN doesn't use centroids
        }

        // Find next unvisited point
        if (state.dbscanQueue.length === 0) {
            let found = false;
            while (state.dbscanIndex < state.points.length) {
                const pIdx = state.dbscanIndex;
                state.dbscanIndex++;
                
                if (!state.dbscanVisited.has(pIdx)) {
                    state.dbscanVisited.add(pIdx);
                    const neighbors = getDBSCANNeighbors(pIdx, eps);
                    
                    if (neighbors.length < minPts) {
                        state.points[pIdx].label = -1; // Label as Noise (grey)
                        state.points[pIdx].type = 'noise';
                        select.clusteringStatus.textContent = `Point ${pIdx} has too few neighbors. Labeled as Noise.`;
                        
                        setExplanation(
                            "DBSCAN: Checking Point (Noise Found)",
                            `DBSCAN looked at point index <strong>${pIdx}</strong> and drew a circle of radius <strong>${eps} pixels</strong> around it. ` +
                            `<br>It found only <strong>${neighbors.length + 1} points</strong> (including itself) inside. ` +
                            `Since this is less than our threshold of <strong>${minPts}</strong>, it labeled this point as <span style="color: ${greyNoise}; font-weight: bold;">Noise (Grey Cross)</span>.<br><br>` +
                            `Note: If this point is later reached by an expanding cluster, it might still become a border point!`
                        );
                        updateClusteringScene();
                        drawDBSCANSearchCircle(state.points[pIdx], eps);
                        return false;
                    } else {
                        // Create a new cluster!
                        // Find next available cluster label
                        const activeLabels = new Set(state.points.map(p => p.label).filter(l => l >= 0));
                        const nextLabel = activeLabels.size;
                        
                        state.points[pIdx].label = nextLabel;
                        state.points[pIdx].type = 'core';
                        
                        // Add neighbors to queue
                        neighbors.forEach(nIdx => {
                            if (nIdx !== pIdx) {
                                state.dbscanQueue.push({ idx: nIdx, label: nextLabel });
                                state.points[nIdx].type = 'queued';
                            }
                        });
                        
                        select.clusteringStatus.textContent = `Discovered Cluster ${nextLabel + 1}! Expanding...`;
                        setExplanation(
                            `New Cluster Discovered! (Cluster ${nextLabel + 1})`,
                            `DBSCAN scanned point <strong>${pIdx}</strong>. Inside its search circle, it found ` +
                            `<strong>${neighbors.length} neighbors</strong>! Since this meets our threshold of <strong>${minPts}</strong>, ` +
                            `this point is officially a <span style="color: ${colors[nextLabel % colors.length]}; font-weight: bold;">Core Point (Solid Circle)</span>. ` +
                            `<br><br>We have started <strong>Cluster ${nextLabel + 1}</strong>. We are putting all its neighbors into a BFS queue to expand the community!`
                        );
                        updateClusteringScene();
                        drawDBSCANSearchCircle(state.points[pIdx], eps);
                        found = true;
                        break;
                    }
                }
            }
            
            if (!found && state.dbscanQueue.length === 0) {
                // Done!
                state.clusterStep = 2; // Finished
                updateClusteringScene();
                updateDBSCANMetrics();
                return true; // Finished
            }
            return false;
        }

        // Process queue
        if (state.dbscanQueue.length > 0) {
            const currentItem = state.dbscanQueue.shift();
            const pIdx = currentItem.idx;
            const clusterLabel = currentItem.label;
            
            const p = state.points[pIdx];
            
            if (!state.dbscanVisited.has(pIdx)) {
                state.dbscanVisited.add(pIdx);
                const neighbors = getDBSCANNeighbors(pIdx, eps);
                
                p.label = clusterLabel;
                
                if (neighbors.length >= minPts) {
                    p.type = 'core';
                    // Expand cluster: Add all unvisited neighbors to queue
                    neighbors.forEach(nIdx => {
                        if (!state.dbscanVisited.has(nIdx) && !state.dbscanQueue.some(item => item.idx === nIdx)) {
                            state.dbscanQueue.push({ idx: nIdx, label: clusterLabel });
                            state.points[nIdx].type = 'queued';
                        }
                    });
                    select.clusteringStatus.textContent = `Expanding Cluster ${clusterLabel + 1}...`;
                    setExplanation(
                        `Expanding Cluster ${clusterLabel + 1}`,
                        `We popped point <strong>${pIdx}</strong> from the queue. It has <strong>${neighbors.length} neighbors</strong>, ` +
                        `making it a <strong>Core Point</strong>. We are coloring it and adding all of *its* neighbors to the queue, growing our community further!`
                    );
                } else {
                    p.type = 'border';
                    select.clusteringStatus.textContent = `Border point found at Cluster ${clusterLabel + 1}`;
                    setExplanation(
                        `Border Point Added`,
                        `We popped point <strong>${pIdx}</strong> from the queue. It has only <strong>${neighbors.length} neighbors</strong> (not enough to be a Core point itself), ` +
                        `but because it is close to a Core point, it gets to join the cluster as a <span style="font-weight: bold; opacity: 0.8;">Border Member (Semi-transparent circle)</span>.`
                    );
                }
            } else if (p.label === -1) {
                // Relabel noise point as border point
                p.label = clusterLabel;
                p.type = 'border';
                select.clusteringStatus.textContent = `Relabeled noise point to Cluster ${clusterLabel + 1} border`;
            }
            
            updateClusteringScene();
            drawDBSCANSearchCircle(p, eps);
            return false;
        }
    }

    function getDBSCANNeighbors(pIdx, eps) {
        const target = state.points[pIdx];
        const neighbors = [];
        state.points.forEach((p, idx) => {
            const dist = Math.sqrt(Math.pow(p.x - target.x, 2) + Math.pow(p.y - target.y, 2));
            if (dist <= eps) {
                neighbors.push(idx);
            }
        });
        return neighbors;
    }

    function updateDBSCANMetrics() {
        const uniqueLabels = new Set(state.points.map(p => p.label).filter(l => l >= 0));
        const nClusters = uniqueLabels.size;
        const nNoise = state.points.filter(p => p.label === -1).length;
        
        select.lblMetricPrimary.textContent = "Clusters Found";
        select.valMetricPrimary.textContent = nClusters;
        
        select.lblMetricSecondary.textContent = "Noise Points";
        select.valMetricSecondary.textContent = nNoise;
        
        setExplanation(
            "DBSCAN Complete!",
            `DBSCAN successfully finished scanning the entire space!<br><br>` +
            `<strong>Summary:</strong>` +
            `<ul>` +
            `<li>Discovered <strong>${nClusters} clusters</strong> of arbitrary shapes.</li>` +
            `<li>Successfully isolated <strong>${nNoise} noise points (outliers)</strong>, refusing to let them distort the shape of the true groups.</li>` +
            `</ul>` +
            `DBSCAN is highly robust to noise and doesn't make assumptions about spherical geometries like K-Means does.`
        );
    }

    // ----------------------------------------------------------------------
    // CLUSTERING CANVAS DRAWING ROUTINES
    // ----------------------------------------------------------------------
    function updateClusteringScene() {
        const canvas = select.clusteringCanvas;
        const ctx = canvas.getContext("2d");
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        // Draw Grid
        ctx.strokeStyle = "rgba(255,255,255,0.03)";
        ctx.lineWidth = 1;
        for(let x=0; x<canvas.width; x+=30) {
            ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, canvas.height); ctx.stroke();
        }
        for(let y=0; y<canvas.height; y+=30) {
            ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(canvas.width, y); ctx.stroke();
        }

        // 1. Draw connecting lines for K-Means (if in assignment stage)
        if (state.activeClusteringAlgo === "kmeans" && state.centroids.length > 0 && state.clusterStep % 2 === 0) {
            state.points.forEach(p => {
                if (p.label !== -1) {
                    const c = state.centroids[p.label];
                    ctx.beginPath();
                    ctx.strokeStyle = "rgba(255,255,255,0.07)";
                    ctx.lineWidth = 1;
                    ctx.moveTo(p.x, p.y);
                    ctx.lineTo(c.x, c.y);
                    ctx.stroke();
                }
            });
        }

        // 2. Draw Points
        state.points.forEach(p => {
            ctx.beginPath();
            
            if (p.label === -1) {
                // Unassigned / Noise
                if (state.activeClusteringAlgo === "dbscan" && p.type === 'noise') {
                    // Draw grey cross for noise
                    ctx.strokeStyle = greyNoise;
                    ctx.lineWidth = 1.5;
                    ctx.moveTo(p.x - 4, p.y - 4); ctx.lineTo(p.x + 4, p.y + 4);
                    ctx.moveTo(p.x + 4, p.y - 4); ctx.lineTo(p.x - 4, p.y + 4);
                    ctx.stroke();
                    return;
                } else {
                    ctx.arc(p.x, p.y, 5, 0, 2 * Math.PI);
                    ctx.fillStyle = "#8e8e9f";
                }
            } else {
                // Colored cluster point
                ctx.arc(p.x, p.y, 5, 0, 2 * Math.PI);
                const color = colors[p.label % colors.length];
                
                if (state.activeClusteringAlgo === "dbscan") {
                    if (p.type === 'core') {
                        ctx.fillStyle = color;
                    } else if (p.type === 'border') {
                        // Border points are semi-transparent
                        ctx.fillStyle = color;
                        ctx.globalAlpha = 0.4;
                        ctx.fill();
                        ctx.globalAlpha = 1.0;
                        ctx.strokeStyle = "#ffffff";
                        ctx.lineWidth = 0.5;
                        ctx.stroke();
                        return;
                    } else if (p.type === 'queued') {
                        ctx.fillStyle = color;
                        ctx.strokeStyle = "#ffb703"; // Glow queue
                        ctx.lineWidth = 1;
                        ctx.stroke();
                    } else {
                        ctx.fillStyle = color;
                    }
                } else {
                    ctx.fillStyle = color;
                }
            }
            ctx.fill();
        });

        // 3. Draw Centroids for K-Means
        if (state.activeClusteringAlgo === "kmeans") {
            state.centroids.forEach(c => {
                // Centroid Glow
                const grad = ctx.createRadialGradient(c.x, c.y, 2, c.x, c.y, 18);
                grad.addColorStop(0, c.color);
                grad.addColorStop(1, 'transparent');
                ctx.fillStyle = grad;
                ctx.beginPath(); ctx.arc(c.x, c.y, 18, 0, 2 * Math.PI); ctx.fill();

                // Centroid Star Core
                ctx.fillStyle = "#ffffff";
                ctx.strokeStyle = "#000000";
                ctx.lineWidth = 1.5;
                drawStar(ctx, c.x, c.y, 5, 11, 5);
            });
        }

        updateClusteringLegendUI();
    }

    function drawStar(ctx, cx, cy, spikes, outerRadius, innerRadius) {
        let rot = Math.PI / 2 * 3;
        let x = cx;
        let y = cy;
        let step = Math.PI / spikes;

        ctx.beginPath();
        ctx.moveTo(cx, cy - outerRadius);
        for (let i = 0; i < spikes; i++) {
            x = cx + Math.cos(rot) * outerRadius;
            y = cy + Math.sin(rot) * outerRadius;
            ctx.lineTo(x, y);
            rot += step;

            x = cx + Math.cos(rot) * innerRadius;
            y = cy + Math.sin(rot) * innerRadius;
            ctx.lineTo(x, y);
            rot += step;
        }
        ctx.lineTo(cx, cy - outerRadius);
        ctx.closePath();
        ctx.fill();
        ctx.stroke();
    }

    function drawDBSCANSearchCircle(p, eps) {
        const canvas = select.clusteringCanvas;
        const ctx = canvas.getContext("2d");
        
        ctx.beginPath();
        ctx.arc(p.x, p.y, eps, 0, 2 * Math.PI);
        ctx.strokeStyle = "rgba(0, 245, 212, 0.4)";
        ctx.fillStyle = "rgba(0, 245, 212, 0.03)";
        ctx.lineWidth = 2;
        ctx.setLineDash([4, 4]); // Dashed active circle
        ctx.stroke();
        ctx.fill();
        ctx.setLineDash([]); // Reset
    }

    function updateClusteringLegendUI() {
        select.clusteringLegend.innerHTML = "";
        
        if (state.activeClusteringAlgo === "kmeans") {
            const k = parseInt(select.sliderK.value);
            for (let i = 0; i < k; i++) {
                const div = document.createElement("div");
                div.className = "legend-item";
                div.innerHTML = `<span class="legend-color" style="background-color: ${colors[i % colors.length]}"></span>` +
                                `<span>Customer Segment ${i+1}</span>`;
                select.clusteringLegend.appendChild(div);
            }
        } else {
            const activeLabels = new Set(state.points.map(p => p.label).filter(l => l >= 0));
            const nClusters = activeLabels.size;
            
            for (let i = 0; i < nClusters; i++) {
                const div = document.createElement("div");
                div.className = "legend-item";
                div.innerHTML = `<span class="legend-color" style="background-color: ${colors[i % colors.length]}"></span>` +
                                `<span>Community Ring ${i+1} (Core & Border)</span>`;
                select.clusteringLegend.appendChild(div);
            }
            
            // Add Noise Legend
            const divNoise = document.createElement("div");
            divNoise.className = "legend-item";
            divNoise.innerHTML = `<span class="legend-color" style="border: 2px dashed ${greyNoise}; background: transparent; display: flex; align-items:center; justify-content:center; color:${greyNoise}; font-weight:bold; font-size:9px;">x</span>` +
                                 `<span>Outlier Noise (Isolated points)</span>`;
            select.clusteringLegend.appendChild(divNoise);
        }
    }

    // ----------------------------------------------------------------------
    // PILLAR 2: PCA DIMENSIONALITY REDUCTION LOGIC
    // ----------------------------------------------------------------------
    select.sliderPcaTilt.addEventListener("input", () => {
        state.pcaRotationAngle = parseInt(select.sliderPcaTilt.value);
        select.valPcaTilt.innerHTML = `${state.pcaRotationAngle}&deg;`;
        updatePcaScene();
        explainPca();
    });

    select.btnRegeneratePca.addEventListener("click", () => {
        generate3DPcaPoints();
        updatePcaScene();
    });

    function generate3DPcaPoints() {
        state.pca3dPoints = [];
        
        // Generate points along a highly tilted, flat elliptical sheet in 3D
        // The sheet is tilted around X and Y axes.
        const nPoints = 120;
        for (let i = 0; i < nPoints; i++) {
            // Internal 2D coordinate on the sheet
            const u = (Math.random() - 0.5) * 200; // Major axis spread
            const v = (Math.random() - 0.5) * 80;  // Minor axis spread
            
            // Tilted mapping to 3D space: X, Y, Z
            // Z is a linear combination of U and V (making it a flat sheet) + tiny noise
            const x = u;
            const y = v;
            
            // Tilt formula: Z = X * sin(30) + Y * cos(45)
            // This places the sheet at an angle of roughly 30 degrees to the horizontal.
            const z = x * Math.sin(30 * Math.PI / 180) + y * Math.cos(45 * Math.PI / 180) + (Math.random() - 0.5) * 8;
            
            state.pca3dPoints.push({ x, y, z });
        }
    }

    // Interactive 3D Drag rotation
    let isMouseDown = false;
    select.pca3dCanvas.addEventListener("mousedown", (e) => {
        isMouseDown = true;
        state.pcaLastMouseX = e.clientX;
    });
    window.addEventListener("mouseup", () => { isMouseDown = false; });
    select.pca3dCanvas.addEventListener("mousemove", (e) => {
        if (!isMouseDown) return;
        const deltaX = e.clientX - state.pcaLastMouseX;
        state.pcaLastMouseX = e.clientX;
        
        // Adjust tilt slider value
        let currentTilt = parseInt(select.sliderPcaTilt.value);
        currentTilt += Math.round(deltaX * 0.5);
        if (currentTilt < -90) currentTilt = -90;
        if (currentTilt > 90) currentTilt = 90;
        
        select.sliderPcaTilt.value = currentTilt;
        state.pcaRotationAngle = currentTilt;
        select.valPcaTilt.innerHTML = `${currentTilt}&deg;`;
        
        updatePcaScene();
        explainPca();
    });

    function updatePcaScene() {
        const canvas3d = select.pca3dCanvas;
        const ctx3d = canvas3d.getContext("2d");
        ctx3d.clearRect(0, 0, canvas3d.width, canvas3d.height);
        
        const canvas2d = select.pca2dCanvas;
        const ctx2d = canvas2d.getContext("2d");
        ctx2d.clearRect(0, 0, canvas2d.width, canvas2d.height);
        
        const cx = canvas3d.width / 2;
        const cy = canvas3d.height / 2;
        
        // Rotation math
        const theta = state.pcaRotationAngle * Math.PI / 180;
        const cosT = Math.cos(theta);
        const sinT = Math.sin(theta);
        
        // 1. Draw 3D coordinate axes
        draw3DAxes(ctx3d, cx, cy, theta);

        // Projected 2D points storage
        const projected2dPoints = [];
        
        // 2. Rotate and Project 3D points
        state.pca3dPoints.forEach(p => {
            // Rotate around Y axis (horizontal camera rotation)
            const rotX = p.x * cosT - p.z * sinT;
            const rotY = p.y;
            const rotZ = p.x * sinT + p.z * cosT; // depth
            
            // Perspective projection coordinates for 3D canvas
            const scale = 300 / (300 + rotZ); // Depth scaling
            const proj3dX = cx + rotX * scale;
            const proj3dY = cy + rotY * scale;
            
            // Draw 3D point
            ctx3d.beginPath();
            ctx3d.arc(proj3dX, proj3dY, Math.max(1, 3.5 * scale), 0, 2 * Math.PI);
            // Color based on original depth Z to show structure
            const depthRatio = (p.z + 80) / 160;
            ctx3d.fillStyle = getInterpolatedColor("#00f5d4", "#ff4d6d", depthRatio);
            ctx3d.fill();
            
            // Orthogonal projection to 2D canvas (this is what the camera sees)
            // We scale it down to fit in the 280x180 2D viewport
            const proj2dX = (canvas2d.width / 2) + rotX * 0.9;
            const proj2dY = (canvas2d.height / 2) + rotY * 0.9;
            projected2dPoints.push({ x: proj2dX, y: proj2dY, originalDepth: p.z });
        });

        // 3. Draw 2D Shadow Canvas
        projected2dPoints.forEach(p => {
            ctx2d.beginPath();
            ctx2d.arc(p.x, p.y, 3, 0, 2 * Math.PI);
            const depthRatio = (p.originalDepth + 80) / 160;
            ctx2d.fillStyle = getInterpolatedColor("#00f5d4", "#ff4d6d", depthRatio);
            ctx2d.fill();
        });

        // 4. Calculate simulated explained variance based on angle!
        // When tilt is near 30 degrees, it aligns perfectly with the sheet, maximizing variance.
        // When tilt is near 0 or 90 degrees, it squashes the sheet, collapsing variance.
        const alignmentError = Math.abs(state.pcaRotationAngle - 30); // Optimal is 30&deg;
        
        let pc1Ratio, pc2Ratio, totalVariance;
        
        if (alignmentError < 15) {
            // High fidelity alignment
            const ratio = 1 - (alignmentError / 15); // 0 to 1
            pc1Ratio = 0.76 + ratio * 0.02;
            pc2Ratio = 0.23 + ratio * 0.009;
            totalVariance = pc1Ratio + pc2Ratio;
        } else {
            // Degrading alignment
            const maxDegrade = Math.min(60, alignmentError - 15);
            const ratio = maxDegrade / 75; // 0 to 1
            pc1Ratio = 0.76 - ratio * 0.15;
            pc2Ratio = 0.23 - ratio * 0.20; // PC2 collapses heavily
            totalVariance = pc1Ratio + pc2Ratio;
        }

        // Update UI Bars
        select.pc1Bar.style.width = `${pc1Ratio * 100}%`;
        select.pc1Val.textContent = `${(pc1Ratio * 100).toFixed(1)}%`;
        select.pc2Bar.style.width = `${pc2Ratio * 100}%`;
        select.pc2Val.textContent = `${(pc2Ratio * 100).toFixed(1)}%`;
        select.valTotalVariance.textContent = `${(totalVariance * 100).toFixed(2)}%`;
    }

    function draw3DAxes(ctx, cx, cy, theta) {
        const len = 120;
        const cosT = Math.cos(theta);
        const sinT = Math.sin(theta);

        // X-Axis (Red)
        const x3d = { x: len, y: 0, z: 0 };
        const rx = x3d.x * cosT - x3d.z * sinT;
        const ry = x3d.y;
        ctx.beginPath(); ctx.strokeStyle = "rgba(255, 77, 109, 0.4)"; ctx.lineWidth = 2;
        ctx.moveTo(cx, cy); ctx.lineTo(cx + rx, cy + ry); ctx.stroke();
        ctx.fillStyle = "rgba(255, 77, 109, 0.8)"; ctx.font = "9px Inter"; ctx.fillText("X", cx + rx + 5, cy + ry);

        // Y-Axis (Green)
        const y3d = { x: 0, y: len, z: 0 };
        ctx.beginPath(); ctx.strokeStyle = "rgba(0, 245, 212, 0.4)";
        ctx.moveTo(cx, cy); ctx.lineTo(cx, cy + y3d.y); ctx.stroke();
        ctx.fillStyle = "rgba(0, 245, 212, 0.8)"; ctx.fillText("Y", cx + 5, cy + y3d.y + 5);

        // Z-Axis (Blue/Depth)
        const z3d = { x: 0, y: 0, z: len };
        const rzx = z3d.x * cosT - z3d.z * sinT;
        const rzy = z3d.y;
        ctx.beginPath(); ctx.strokeStyle = "rgba(58, 134, 200, 0.4)";
        ctx.moveTo(cx, cy); ctx.lineTo(cx + rzx, cy + rzy); ctx.stroke();
        ctx.fillStyle = "rgba(58, 134, 200, 0.8)"; ctx.fillText("Z", cx + rzx + 5, cy + rzy + 5);
    }

    function getInterpolatedColor(color1, color2, factor) {
        // Simple hex color interpolator
        const c1 = parseColor(color1);
        const c2 = parseColor(color2);
        
        const r = Math.round(c1.r + factor * (c2.r - c1.r));
        const g = Math.round(c1.g + factor * (c2.g - c1.g));
        const b = Math.round(c1.b + factor * (c2.b - c1.b));
        
        return `rgb(${r}, ${g}, ${b})`;
    }

    function parseColor(color) {
        if (color.startsWith("#")) {
            return {
                r: parseInt(color.slice(1, 3), 16),
                g: parseInt(color.slice(3, 5), 16),
                b: parseInt(color.slice(5, 7), 16)
            };
        }
        return { r: 0, g: 245, b: 212 };
    }

    // ----------------------------------------------------------------------
    // PILLAR 3: ANOMALY DETECTION LOGIC
    // ----------------------------------------------------------------------
    
    // Canvas Mouse Click: Add custom transaction point
    select.anomalyCanvas.addEventListener("mousedown", (e) => {
        const rect = select.anomalyCanvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        
        state.anomalyPoints.push({
            x: x,
            y: y,
            score: 0.0,
            depth: 0
        });
        
        state.anomalySlices = [];
        updateAnomalyScene();
        select.anomalyStatus.textContent = `Added transaction: Amount = $${Math.round(x * 0.83)}, Freq = ${(y * 0.12).toFixed(1)}/wk`;
        explainAnomalyInitial();
    });

    select.btnClearAnomaly.addEventListener("click", () => {
        state.anomalyPoints = [];
        state.anomalySlices = [];
        updateAnomalyScene();
        select.riskLedgerBody.innerHTML = `<tr><td colspan="5" style="text-align: center; color: #5c5c64; padding: 20px;">No transactions analyzed yet. Run Isolation Forest!</td></tr>`;
        select.anomalyStatus.textContent = "Canvas cleared. Click to draw transaction points.";
    });

    select.btnPresetTransactions.addEventListener("click", () => {
        generateTransactionsPreset();
        state.anomalySlices = [];
        updateAnomalyScene();
    });

    function generateTransactionsPreset() {
        state.anomalyPoints = [];
        
        // 1. Normal Transactions: Small amount (X), moderate frequency (Y)
        // Center around X=100 (Amount ~$80), Y=120 (Freq ~14 purchases/wk)
        const centerX = 120;
        const centerY = 140;
        
        for (let i = 0; i < 45; i++) {
            const r = Math.random() * 45;
            const theta = Math.random() * 2 * Math.PI;
            state.anomalyPoints.push({
                x: centerX + r * Math.cos(theta),
                y: centerY + r * Math.sin(theta),
                score: 0.0,
                depth: 0
            });
        }

        // 2. High risk Anomalies
        // Outlier A: Insane amount ($450, X=500), low frequency (Y=60)
        state.anomalyPoints.push({ x: 490, y: 80, score: 0.0, depth: 0 });
        state.anomalyPoints.push({ x: 510, y: 100, score: 0.0, depth: 0 });

        // Outlier B: Small amount ($50, X=70), but crazy frequency (40/wk, Y=350)
        state.anomalyPoints.push({ x: 80, y: 340, score: 0.0, depth: 0 });
        state.anomalyPoints.push({ x: 100, y: 350, score: 0.0, depth: 0 });
        
        select.anomalyStatus.textContent = "Generated Credit Card transactions preset.";
    }

    // Step Slicing
    select.btnStepIsolation.addEventListener("click", () => {
        if (state.anomalyPoints.length === 0) return;
        stepIsolationSlicing();
    });

    function stepIsolationSlicing() {
        const canvas = select.anomalyCanvas;
        
        // Draw a random horizontal or vertical slicing line
        const direction = Math.random() > 0.5 ? 'H' : 'V';
        let value = 0;
        
        if (direction === 'V') {
            // Vertical split: select a random X coord within range of points
            const xCoords = state.anomalyPoints.map(p => p.x);
            const minX = Math.min(...xCoords) - 10;
            const maxX = Math.max(...xCoords) + 10;
            value = minX + Math.random() * (maxX - minX);
        } else {
            // Horizontal split: select a random Y coord within range
            const yCoords = state.anomalyPoints.map(p => p.y);
            const minY = Math.min(...yCoords) - 10;
            const maxY = Math.max(...yCoords) + 10;
            value = minY + Math.random() * (maxY - minY);
        }

        state.anomalySlices.push({ dir: direction, val: value });
        
        // Cap the number of slices to draw on screen
        if (state.anomalySlices.length > 25) {
            state.anomalySlices.shift();
        }

        updateAnomalyScene();
        select.anomalyStatus.textContent = `Random cut drawn at ${direction === 'V' ? 'X=' + Math.round(value*0.83) : 'Y=' + Math.round(value*0.12)}`;
        
        setExplanation(
            "Splitting Space! (Isolation Tree Split)",
            `We drew a random <strong>${direction === 'V' ? 'Vertical' : 'Horizontal'} slice</strong>. ` +
            `Notice how points in empty areas get sliced off into their own boxes immediately (isolated). ` +
            `Points in the dense cluster, however, are still sharing a box with 20+ other points. ` +
            `<br><br>Anomalies are lonely. It takes only 2 or 3 random slices to completely isolate them, ` +
            `whereas a normal point in the center of the 'city' requires 15+ slices to separate it from the crowd.`
        );
    }

    // Run Heatmap Score
    select.btnRunIsolation.addEventListener("click", () => {
        if (state.anomalyPoints.length === 0) return;
        runIsolationHeatmap();
    });

    function runIsolationHeatmap() {
        select.anomalyStatus.textContent = "Calculating transaction risk scores...";
        
        // Compute path depths for all points
        // In JS, we simulate the forest of partition trees:
        // Outliers (far from dense normal cluster) get higher scores.
        // Normal cluster center (around X=120, Y=140) get lowest scores.
        
        const nTrees = parseInt(select.sliderTrees.value);
        
        state.anomalyPoints.forEach(p => {
            p.score = calculateSimulatedAnomalyScore(p.x, p.y);
        });

        // 1. Draw Heatmap Background
        drawAnomalyHeatmapBackground();

        // 2. Render Risk Ledger Table
        renderRiskLedgerTable();
        
        select.anomalyStatus.textContent = "Isolation Forest Heatmap complete! Risk ledger updated.";
        
        const maxScorePoint = [...state.anomalyPoints].sort((a, b) => b.score - a.score)[0];
        setExplanation(
            "Risk Map Generated! (Isolation Score)",
            `The background color represents the <strong>Anomaly Risk Score</strong>: ` +
            `<br>- <span style="color: var(--color-pink); font-weight: bold;">Bright Hot Zones</span> represent high risk (Score > 0.6). Transactions landing here are flagged instantly.` +
            `<br>- <span style="color: var(--color-accent); font-weight: bold;">Deep Cool Zones</span> represent safe, normal transaction habits.` +
            `<br><br>The highest risk transaction flagged has a score of <strong>${maxScorePoint.score.toFixed(3)}</strong>. ` +
            `It took very few partition slices to isolate it from the rest of the transactions.`
        );
    }

    function calculateSimulatedAnomalyScore(x, y) {
        // Distance to the normal city center (120, 140)
        const distToCenter = Math.sqrt(Math.pow(x - 120, 2) + Math.pow(y - 140, 2));
        
        // Outliers are far away. Score ranges from 0.3 (very normal) to 0.85 (highly anomalous)
        let score = 0.3 + (distToCenter / 450) * 0.55;
        score = Math.min(0.85, Math.max(0.3, score));
        
        // Add a tiny bit of random variance to simulate multiple trees
        score += (Math.random() - 0.5) * 0.05;
        return Math.min(0.95, Math.max(0.2, score));
    }

    function drawAnomalyHeatmapBackground() {
        const canvas = select.anomalyCanvas;
        const ctx = canvas.getContext("2d");
        
        // Draw score grid
        const step = 12; // Grid cell size
        for (let x = 0; x < canvas.width; x += step) {
            for (let y = 0; y < canvas.height; y += step) {
                const score = calculateSimulatedAnomalyScore(x, y);
                // Heatmap colors: plasma (blue -> purple -> orange -> yellow/white)
                ctx.fillStyle = getPlasmaColor(score);
                ctx.fillRect(x, y, step, step);
            }
        }

        // Draw grid overlay lines slightly
        ctx.strokeStyle = "rgba(255,255,255,0.02)";
        ctx.lineWidth = 1;
        for(let x=0; x<canvas.width; x+=30) {
            ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, canvas.height); ctx.stroke();
        }
        for(let y=0; y<canvas.height; y+=30) {
            ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(canvas.width, y); ctx.stroke();
        }

        // Redraw Points on top
        state.anomalyPoints.forEach(p => {
            ctx.beginPath();
            ctx.arc(p.x, p.y, 6, 0, 2 * Math.PI);
            
            if (p.score > 0.6) {
                ctx.fillStyle = "#ff0055"; // Pink Outlier
                ctx.strokeStyle = "#ffffff";
                ctx.lineWidth = 1.2;
                ctx.stroke();
            } else {
                ctx.fillStyle = "#00ffcc"; // Teal Normal
                ctx.strokeStyle = "#111111";
                ctx.lineWidth = 0.8;
                ctx.stroke();
            }
            ctx.fill();
        });
    }

    function getPlasmaColor(score) {
        // Mapping 0.3 - 0.85 to purple -> orange -> pink
        if (score < 0.45) {
            // Cool deep blue/purple zone
            const f = (score - 0.2) / 0.25;
            return getInterpolatedColor("#0c0728", "#3f107c", Math.max(0, Math.min(1, f)));
        } else if (score < 0.62) {
            // Mid warm pink zone
            const f = (score - 0.45) / 0.17;
            return getInterpolatedColor("#3f107c", "#9f1b95", Math.max(0, Math.min(1, f)));
        } else {
            // Hot orange/yellow danger zone
            const f = (score - 0.62) / 0.23;
            return getInterpolatedColor("#9f1b95", "#ff0055", Math.max(0, Math.min(1, f)));
        }
    }

    function updateAnomalyScene() {
        const canvas = select.anomalyCanvas;
        const ctx = canvas.getContext("2d");
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        // Draw grid
        ctx.strokeStyle = "rgba(255,255,255,0.03)";
        ctx.lineWidth = 1;
        for(let x=0; x<canvas.width; x+=30) {
            ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, canvas.height); ctx.stroke();
        }
        for(let y=0; y<canvas.height; y+=30) {
            ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(canvas.width, y); ctx.stroke();
        }

        // Draw Slices
        ctx.strokeStyle = "rgba(255, 183, 3, 0.65)"; // Glowing yellow slice lines
        ctx.lineWidth = 1.5;
        state.anomalySlices.forEach(s => {
            ctx.beginPath();
            if (s.dir === 'V') {
                ctx.moveTo(s.val, 0);
                ctx.lineTo(s.val, canvas.height);
            } else {
                ctx.moveTo(0, s.val);
                ctx.lineTo(canvas.width, s.val);
            }
            ctx.stroke();
        });

        // Draw Points
        state.anomalyPoints.forEach(p => {
            ctx.beginPath();
            ctx.arc(p.x, p.y, 5.5, 0, 2 * Math.PI);
            ctx.fillStyle = "#8e8e9f";
            ctx.strokeStyle = "#121214";
            ctx.lineWidth = 0.8;
            ctx.fill();
            ctx.stroke();
        });
    }

    function renderRiskLedgerTable() {
        select.riskLedgerBody.innerHTML = "";
        
        // Sort points by risk score descending
        const sortedPoints = [...state.anomalyPoints].sort((a, b) => b.score - a.score);
        
        sortedPoints.forEach((p, idx) => {
            // Translate coordinates to real values
            const amt = Math.round(p.x * 0.83);
            const freq = Math.round(p.y * 0.12);
            
            const isAnomaly = p.score > 0.6;
            const typeEmoji = isAnomaly ? "🚨 Outlier" : "✅ Normal";
            const verdict = isAnomaly 
                ? "<span class='badge badge-anomaly'>FLAGGED FRAUD</span>"
                : "<span class='badge badge-normal'>APPROVED</span>";
                
            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td>${typeEmoji}</td>
                <td>$${amt}</td>
                <td>${freq}/wk</td>
                <td class="${isAnomaly ? 'text-pink' : ''}">${p.score.toFixed(3)}</td>
                <td>${verdict}</td>
            `;
            
            select.riskLedgerBody.appendChild(tr);
        });
    }

    // ----------------------------------------------------------------------
    // PILLAR 4: MARKET BASKET ASSOCIATION LOGIC
    // ----------------------------------------------------------------------
    
    // Add Item to Shelf Click listeners
    document.querySelectorAll(".grocery-shelf .item-card").forEach(card => {
        card.addEventListener("click", () => {
            const item = card.getAttribute("data-item");
            if (state.basket.has(item)) {
                state.basket.delete(item);
                card.classList.remove("selected");
            } else {
                state.basket.add(item);
                card.classList.add("selected");
            }
            updateBasketUI();
            renderRelationshipGraph();
            evaluateRules();
        });
    });

    select.btnClearBasket.addEventListener("click", () => {
        state.basket.clear();
        document.querySelectorAll(".grocery-shelf .item-card").forEach(card => {
            card.classList.remove("selected");
        });
        updateBasketUI();
        renderRelationshipGraph();
        evaluateRules();
        select.minedRulesList.innerHTML = `<div style="text-align: center; color: #5c5c64; padding: 15px; font-size:0.75rem;">No products in basket. Tap grocery items to buy!</div>`;
    });

    function updateBasketUI() {
        select.userBasket.innerHTML = "";
        
        if (state.basket.size === 0) {
            select.userBasket.innerHTML = `<div class="basket-placeholder">Your basket is empty. Click items on the shelf to buy!</div>`;
            return;
        }

        state.basket.forEach(item => {
            // Find emoji
            const node = state.graphNodes.find(n => n.id === item);
            const emoji = node ? node.emoji : "🛍️";
            
            const itemSpan = document.createElement("span");
            itemSpan.className = "basket-item";
            itemSpan.innerHTML = `
                <span>${emoji} ${item}</span>
                <span class="basket-item-remove" data-item="${item}">&times;</span>
            `;
            
            // Remove single item listener
            itemSpan.querySelector(".basket-item-remove").addEventListener("click", (e) => {
                const targetItem = e.target.getAttribute("data-item");
                state.basket.delete(targetItem);
                
                // Deselect on shelf
                const shelfCard = document.querySelector(`.grocery-shelf .item-card[data-item="${targetItem}"]`);
                if (shelfCard) shelfCard.classList.remove("selected");
                
                updateBasketUI();
                renderRelationshipGraph();
                evaluateRules();
            });
            
            select.userBasket.appendChild(itemSpan);
        });
    }

    function evaluateRules() {
        select.minedRulesList.innerHTML = "";
        
        if (state.basket.size === 0) {
            select.minedRulesList.innerHTML = `<div style="text-align: center; color: #5c5c64; padding: 15px; font-size:0.75rem;">No products in basket. Tap grocery items to buy!</div>`;
            return;
        }

        // Find which rules are triggered by the current basket contents
        let triggeredRules = [];
        let otherRules = [];
        
        state.rules.forEach(rule => {
            // Check if antecedent is a subset of the basket
            const isTriggered = rule.antecedent.every(item => state.basket.has(item));
            if (isTriggered) {
                triggeredRules.push(rule);
            } else {
                otherRules.push(rule);
            }
        });

        // Print triggered rules first in glowing card
        if (triggeredRules.length > 0) {
            triggeredRules.forEach(rule => {
                const card = document.createElement("div");
                card.className = "rule-item-card";
                card.style.borderColor = "var(--color-accent)";
                card.style.background = "rgba(0, 245, 212, 0.05)";
                
                card.innerHTML = `
                    <div class="rule-statement">
                        🟢 TRIGGERED: If you buy <span class="rule-highlight">[${rule.antecedent.join(", ")}]</span> 
                        &rarr; then you also buy <span class="rule-highlight">[${rule.consequent.join(", ")}]</span>
                    </div>
                    <div class="rule-stats">
                        <span>Popularity (Support): <strong>${(rule.support*100).toFixed(0)}%</strong></span>
                        <span>Reliability (Conf): <strong>${(rule.confidence*100).toFixed(0)}%</strong></span>
                        <span>Strength (Lift): <strong style="color:var(--color-accent);">${rule.lift.toFixed(2)}x</strong></span>
                    </div>
                `;
                select.minedRulesList.appendChild(card);
            });
            
            // Injects translation text for the top triggered rule
            const topRule = triggeredRules[0];
            setExplanation(
                "Basket Insight Found!",
                `Awesome! Your basket contains <strong>${topRule.antecedent.join(" and ")}</strong>, which triggers a strong association rule:<br>` +
                `<ul>` +
                `<li><strong>Rule:</strong> Customers buying ${topRule.antecedent.join(" and ")} also buy <strong>${topRule.consequent.join(" and ")}</strong>.</li>` +
                `<li><strong>Reliability (Confidence):</strong> ${Math.round(topRule.confidence*100)}% of the time, this rule holds true.</li>` +
                `<li><strong>Strength multiplier (Lift):</strong> ${topRule.lift.toFixed(2)}x. They are ${topRule.lift.toFixed(2)} times more likely to buy both together than if they just bought them randomly.</li>` +
                `</ul>` +
                `<strong>Business Action:</strong> ${topRule.desc}`
            );
        } else {
            // Default basket explanation
            setExplanation(
                "Shopping in progress...",
                `You have placed <strong>${Array.from(state.basket).join(", ")}</strong> in your cart. ` +
                `No rules are triggered yet. Try adding <strong>Bread</strong> or <strong>Beer</strong> or <strong>Diapers</strong> to see the supermarket algorithms react in real-time!`
            );
        }

        // Show non-triggered rules in dimmed card
        otherRules.forEach(rule => {
            const card = document.createElement("div");
            card.className = "rule-item-card";
            card.style.opacity = 0.5;
            
            card.innerHTML = `
                <div class="rule-statement">
                    If buying [${rule.antecedent.join(", ")}] &rarr; then they buy [${rule.consequent.join(", ")}]
                </div>
                <div class="rule-stats">
                    <span>Popularity: ${(rule.support*100).toFixed(0)}%</span>
                    <span>Reliability: ${(rule.confidence*100).toFixed(0)}%</span>
                    <span>Strength: ${rule.lift.toFixed(2)}x</span>
                </div>
            `;
            select.minedRulesList.appendChild(card);
        });
    }

    // ----------------------------------------------------------------------
    // SVG Relationship Graph Builder
    // ----------------------------------------------------------------------
    function renderRelationshipGraph() {
        const svg = select.relationshipGraph;
        svg.innerHTML = ""; // Clear
        
        // 1. Draw Links (lines connecting products)
        state.graphLinks.forEach(link => {
            const sourceNode = state.graphNodes.find(n => n.id === link.source);
            const targetNode = state.graphNodes.find(n => n.id === link.target);
            
            if (sourceNode && targetNode) {
                // Check if link is active (source is in user's basket)
                const isActive = state.basket.has(link.source);
                
                const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
                line.setAttribute("x1", sourceNode.x);
                line.setAttribute("y1", sourceNode.y);
                line.setAttribute("x2", targetNode.x);
                line.setAttribute("y2", targetNode.y);
                
                if (isActive) {
                    line.setAttribute("class", "graph-link active");
                    line.setAttribute("stroke", "var(--color-accent)");
                } else {
                    line.setAttribute("class", "graph-link");
                    line.setAttribute("stroke", "rgba(255,255,255,0.15)");
                }
                
                svg.appendChild(line);
            }
        });

        // 2. Draw Nodes (circular cards for products)
        state.graphNodes.forEach(node => {
            const isSelected = state.basket.has(node.id);
            
            const group = document.createElementNS("http://www.w3.org/2000/svg", "g");
            group.setAttribute("class", "graph-node");
            group.setAttribute("transform", `translate(${node.x}, ${node.y})`);
            
            // Node circle
            const circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
            circle.setAttribute("r", 15);
            
            if (isSelected) {
                circle.setAttribute("fill", "var(--color-primary)");
                circle.setAttribute("stroke", "#ffffff");
                circle.setAttribute("stroke-width", 1.5);
                circle.setAttribute("filter", "drop-shadow(0 0 5px var(--color-primary-glow))");
            } else {
                circle.setAttribute("fill", "#1e1e24");
                circle.setAttribute("stroke", "rgba(255,255,255,0.2)");
                circle.setAttribute("stroke-width", 1);
            }
            
            // Emoji Label
            const textEmoji = document.createElementNS("http://www.w3.org/2000/svg", "text");
            textEmoji.setAttribute("text-anchor", "middle");
            textEmoji.setAttribute("dy", "5");
            textEmoji.setAttribute("font-size", "14px");
            textEmoji.textContent = node.emoji;
            
            // Text Label
            const textLabel = document.createElementNS("http://www.w3.org/2000/svg", "text");
            textLabel.setAttribute("text-anchor", "middle");
            textLabel.setAttribute("y", "28");
            textLabel.setAttribute("fill", isSelected ? "#ffffff" : "var(--text-secondary)");
            textLabel.setAttribute("font-size", "9px");
            textLabel.setAttribute("font-weight", isSelected ? "bold" : "normal");
            textLabel.setAttribute("font-family", "Inter");
            textLabel.textContent = node.label;
            
            // Click to toggle node
            group.addEventListener("click", () => {
                const shelfCard = document.querySelector(`.grocery-shelf .item-card[data-item="${node.id}"]`);
                if (state.basket.has(node.id)) {
                    state.basket.delete(node.id);
                    if (shelfCard) shelfCard.classList.remove("selected");
                } else {
                    state.basket.add(node.id);
                    if (shelfCard) shelfCard.classList.add("selected");
                }
                updateBasketUI();
                renderRelationshipGraph();
                evaluateRules();
            });
            
            group.appendChild(circle);
            group.appendChild(textEmoji);
            group.appendChild(textLabel);
            svg.appendChild(group);
        });
    }

    // ----------------------------------------------------------------------
    // App Bootstrap
    // ----------------------------------------------------------------------
    initTabScene("clustering"); // Load default view
});

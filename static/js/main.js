// Global State
let currentTrack = null;
let isPlaying = false;
const audioPlayer = document.getElementById('audio-player');

document.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('access_token');
    if (!token && window.location.pathname === '/dashboard') {
        window.location.href = '/login';
        return;
    }

    // Logout
    const logoutBtn = document.getElementById('logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', () => {
            localStorage.clear();
            window.location.href = '/';
        });
    }

    // Dashboard Load
    if (window.location.pathname === '/dashboard') {
        loadMusic();
        loadUserPlan();
        loadLikedSongs();
        setupPlayerListeners();
        setupSearch();
        setupNavigation();
    }

    // Upgrade Modal Logic
    const upgradeBtn = document.getElementById('upgrade-btn');
    const upgradeModal = document.getElementById('upgrade-modal');
    const closeModal = document.getElementById('close-modal');

    if (upgradeBtn) {
        upgradeBtn.addEventListener('click', () => {
            loadPlans();
            upgradeModal.classList.remove('hidden');
        });
    }

    if (closeModal) {
        closeModal.addEventListener('click', () => {
            upgradeModal.classList.add('hidden');
        });
    }
});

function setupNavigation() {
    const navHome = document.getElementById('nav-home');
    const navSearch = document.getElementById('nav-search');
    const navLibrary = document.getElementById('nav-library');
    const navCreatePlaylist = document.getElementById('nav-create-playlist');
    const navLiked = document.getElementById('nav-liked');

    const mainView = document.getElementById('main-view');
    const searchView = document.getElementById('search-view');
    const searchInput = document.getElementById('search-input');

    const resetNav = () => {
        [navHome, navSearch, navLibrary, navCreatePlaylist, navLiked].forEach(el => {
            el.classList.remove('bg-white/10', 'text-white', 'opacity-100');
            el.classList.add('text-zyra-muted', 'hover:text-white', 'hover:bg-white/5');
            // Reset icons if specific styling was added, but text/bg is main part
        });
    };

    const setActive = (el) => {
        resetNav();
        el.classList.remove('text-zyra-muted', 'hover:text-white', 'hover:bg-white/5');
        el.classList.add('bg-white/10', 'text-white', 'opacity-100');
    };

    navHome.addEventListener('click', (e) => {
        e.preventDefault();
        setActive(navHome);
        mainView.classList.remove('hidden');
        searchView.classList.add('hidden');
        // Reset search input
        searchInput.value = '';
        renderHomeContent();
    });

    navSearch.addEventListener('click', (e) => {
        e.preventDefault();
        setActive(navSearch);
        mainView.classList.add('hidden');
        searchView.classList.remove('hidden');
        searchInput.focus();
    });

    navLibrary.addEventListener('click', (e) => {
        e.preventDefault();
        setActive(navLibrary);
        // For MVP, Library shows Liked Songs predominantly + Playlists
        showLibraryView();
    });

    navLiked.addEventListener('click', (e) => {
        e.preventDefault();
        setActive(navLiked);
        showLikedSongsView();
    });

    navCreatePlaylist.addEventListener('click', (e) => {
        e.preventDefault();
        alert('Playlist creation coming soon!');
    });
}

function renderHomeContent() {
    const mainView = document.getElementById('main-view');
    mainView.innerHTML = `
        <h1 class="text-3xl font-bold mb-6">Good evening</h1>
        
        <!-- Featured Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-8">
             <!-- Card 1 -->
                <div class="bg-white/5 hover:bg-white/10 transition rounded-md flex overflow-hidden cursor-pointer group relative">
                    <img src="https://images.unsplash.com/photo-1514525253440-b393452e8d26?w=300&h=300&fit=crop" class="w-20 h-20 object-cover">
                    <div class="flex-1 p-4 flex items-center justify-between">
                        <span class="font-bold">Neon Nights</span>
                        <div class="play-btn-overlay w-10 h-10 bg-zyra-primary rounded-full flex items-center justify-center shadow-xl opacity-0 translate-y-2 group-hover:opacity-100 group-hover:translate-y-0 transition-all duration-300 absolute right-4">
                            <svg class="w-5 h-5 text-black ml-1" fill="currentColor" viewBox="0 0 20 20"><path d="M6.3 2.841A1.5 1.5 0 004 4.11V15.89a1.5 1.5 0 002.3 1.269l9.344-5.89a1.5 1.5 0 000-2.538L6.3 2.84z"/></svg>
                        </div>
                    </div>
                </div>
                <!-- Card 2 -->
                <div class="bg-white/5 hover:bg-white/10 transition rounded-md flex overflow-hidden cursor-pointer group relative">
                     <img src="https://images.unsplash.com/photo-1493225255756-d9584f8606e9?w=300&h=300&fit=crop" class="w-20 h-20 object-cover">
                    <div class="flex-1 p-4 flex items-center justify-between">
                        <span class="font-bold">Deep Focus</span>
                        <div class="w-10 h-10 bg-zyra-primary rounded-full flex items-center justify-center shadow-xl opacity-0 translate-y-2 group-hover:opacity-100 group-hover:translate-y-0 transition-all duration-300 absolute right-4">
                            <svg class="w-5 h-5 text-black ml-1" fill="currentColor" viewBox="0 0 20 20"><path d="M6.3 2.841A1.5 1.5 0 004 4.11V15.89a1.5 1.5 0 002.3 1.269l9.344-5.89a1.5 1.5 0 000-2.538L6.3 2.84z"/></svg>
                        </div>
                    </div>
                </div>
                <!-- Card 3 -->
                 <div class="bg-white/5 hover:bg-white/10 transition rounded-md flex overflow-hidden cursor-pointer group relative">
                     <img src="https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=300&h=300&fit=crop" class="w-20 h-20 object-cover">
                    <div class="flex-1 p-4 flex items-center justify-between">
                        <span class="font-bold">Workout Energy</span>
                        <div class="w-10 h-10 bg-zyra-primary rounded-full flex items-center justify-center shadow-xl opacity-0 translate-y-2 group-hover:opacity-100 group-hover:translate-y-0 transition-all duration-300 absolute right-4">
                            <svg class="w-5 h-5 text-black ml-1" fill="currentColor" viewBox="0 0 20 20"><path d="M6.3 2.841A1.5 1.5 0 004 4.11V15.89a1.5 1.5 0 002.3 1.269l9.344-5.89a1.5 1.5 0 000-2.538L6.3 2.84z"/></svg>
                        </div>
                    </div>
                </div>
        </div>

        <!-- Trending Section -->
        <h2 class="text-2xl font-bold mb-4">Trending Now</h2>
        
        <div class="bg-[#181818] rounded-xl p-6">
            <div class="flex border-b border-gray-700 pb-2 mb-4 text-xs text-zyra-muted tracking-wider uppercase">
                <div class="w-10">#</div>
                <div class="flex-1">Title</div>
                <div class="w-1/3">Album</div>
                <div class="w-24 text-right">Like</div>
                <div class="w-16 text-right"><svg class="w-4 h-4 ml-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/></svg></div>
            </div>
            
            <div id="music-list" class="space-y-2">
                 <div class="text-center py-10 text-zyra-muted">Loading music...</div>
            </div>
        </div>
    `;
    loadMusic(); // Reload music list into the new container
}

async function showLikedSongsView() {
    const mainView = document.getElementById('main-view');
    const searchView = document.getElementById('search-view');
    mainView.classList.remove('hidden');
    searchView.classList.add('hidden');

    // Fetch liked songs
    try {
        const res = await fetchWithAuth('/api/me/liked');
        const likedSongs = await res.json();

        mainView.innerHTML = `
             <div class="flex items-end mb-8 space-x-6 bg-gradient-to-b from-indigo-800 to-transparent p-6 -mx-8 -mt-8">
                <div class="w-52 h-52 bg-gradient-to-br from-indigo-500 to-purple-500 flex items-center justify-center shadow-2xl">
                    <svg class="w-20 h-20 text-white" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z" clip-rule="evenodd"/></svg>
                </div>
                <div>
                    <h2 class="text-xs font-bold uppercase tracking-wider text-white">Playlist</h2>
                    <h1 class="text-6xl font-bold text-white mb-4">Liked Songs</h1>
                    <p class="text-sm text-gray-300 font-semibold">${JSON.parse(localStorage.getItem('user')).username} • ${likedSongs.length} songs</p>
                </div>
             </div>
             
             <div class="bg-[#181818] rounded-xl p-6">
                <div class="flex border-b border-gray-700 pb-2 mb-4 text-xs text-zyra-muted tracking-wider uppercase">
                    <div class="w-10">#</div>
                    <div class="flex-1">Title</div>
                    <div class="w-1/3">Album</div>
                    <div class="w-24 text-right">Like</div>
                    <div class="w-16 text-right"><svg class="w-4 h-4 ml-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/></svg></div>
                </div>
                <div id="liked-list" class="space-y-2"></div>
            </div>
        `;

        renderMusicList(likedSongs, document.getElementById('liked-list'), false);

    } catch (e) {
        console.error(e);
    }
}

function showLibraryView() {
    // Reuse Liked Songs for now as it's the main library feature implemented
    showLikedSongsView();
}

function setupSearch() {
    const searchInput = document.getElementById('search-input');
    const searchView = document.getElementById('search-view');
    const mainView = document.getElementById('main-view');
    const resultsContainer = document.getElementById('search-results');
    let debounceTimer;

    searchInput.addEventListener('input', (e) => {
        clearTimeout(debounceTimer);
        const query = e.target.value.trim();

        if (query.length > 0) {
            mainView.classList.add('hidden');
            searchView.classList.remove('hidden');

            debounceTimer = setTimeout(async () => {
                const res = await fetchWithAuth(`/api/search?q=${query}`);
                const data = await res.json();
                renderMusicList(data, resultsContainer, true); // true = as cards
            }, 300);
        } else {
            mainView.classList.remove('hidden');
            searchView.classList.add('hidden');
        }
    });
}

function setupPlayerListeners() {
    const playPauseBtn = document.getElementById('play-pause-btn');
    const progressBar = document.getElementById('progress-bar');
    const volumeBar = document.getElementById('volume-bar');

    // Play/Pause Toggle
    playPauseBtn.addEventListener('click', togglePlay);

    // Audio Events
    audioPlayer.addEventListener('timeupdate', updateProgress);
    audioPlayer.addEventListener('ended', () => {
        isPlaying = false;
        updatePlayButton();
    });
    audioPlayer.addEventListener('loadedmetadata', () => {
        document.getElementById('duration').textContent = formatTime(audioPlayer.duration);
    });

    // Scrubbing
    progressBar.addEventListener('input', () => {
        const time = (progressBar.value / 100) * audioPlayer.duration;
        audioPlayer.currentTime = time;
    });

    // Volume
    volumeBar.addEventListener('input', () => {
        audioPlayer.volume = volumeBar.value / 100;
    });
}

function togglePlay() {
    if (!currentTrack) return;

    if (audioPlayer.paused) {
        audioPlayer.play();
        isPlaying = true;
    } else {
        audioPlayer.pause();
        isPlaying = false;
    }
    updatePlayButton();
}

function updatePlayButton() {
    const playIcon = document.getElementById('play-icon');
    const pauseIcon = document.getElementById('pause-icon');

    if (isPlaying) {
        playIcon.classList.add('hidden');
        pauseIcon.classList.remove('hidden');
    } else {
        playIcon.classList.remove('hidden');
        pauseIcon.classList.add('hidden');
    }
}

function updateProgress() {
    const progressBar = document.getElementById('progress-bar');
    const currentTimeEl = document.getElementById('current-time');

    if (audioPlayer.duration) {
        const percent = (audioPlayer.currentTime / audioPlayer.duration) * 100;
        progressBar.value = percent;
        currentTimeEl.textContent = formatTime(audioPlayer.currentTime);
    }
}

function formatTime(seconds) {
    const min = Math.floor(seconds / 60);
    const sec = Math.floor(seconds % 60);
    return `${min}:${sec < 10 ? '0' : ''}${sec}`;
}

async function loadUserPlan() {
    const user = JSON.parse(localStorage.getItem('user'));
    const planBadge = document.getElementById('user-plan-badge');
    if (user && user.subscription) {
        planBadge.textContent = user.subscription.plan_name;
    } else {
        planBadge.textContent = 'Free';
    }
}

let likedSongIds = new Set();

async function loadLikedSongs() {
    try {
        const res = await fetchWithAuth('/api/me/liked');
        const data = await res.json();
        likedSongIds = new Set(data.map(s => s.id));
    } catch (e) { console.error(e); }
}

async function loadMusic() {
    try {
        const res = await fetchWithAuth('/api/music');
        const musicList = await res.json();
        renderMusicList(musicList, document.getElementById('music-list'), false);
    } catch (err) {
        console.error(err);
    }
}

function renderMusicList(list, container, asCards) {
    container.innerHTML = '';
    if (list.length === 0) {
        container.innerHTML = '<div class="text-gray-500">No results found</div>';
        return;
    }

    list.forEach((track, index) => {
        const isLiked = likedSongIds.has(track.id);
        const heartClass = isLiked ? 'text-green-500 fill-current' : 'text-gray-400 hover:text-white';

        let html = '';
        if (asCards) {
            // Render as search result cards
            html = `
            <div class="bg-[#181818] p-4 rounded-md hover:bg-[#282828] transition group cursor-pointer relative">
                <div class="relative mb-4">
                    <img src="${track.cover_image}" class="w-full aspect-square object-cover rounded shadow-lg">
                    <button class="play-btn absolute bottom-2 right-2 w-12 h-12 bg-green-500 rounded-full flex items-center justify-center shadow-xl opacity-0 group-hover:opacity-100 transform translate-y-2 group-hover:translate-y-0 transition-all duration-300">
                        <svg class="w-6 h-6 text-black pl-1" fill="currentColor" viewBox="0 0 20 20"><path d="M6.3 2.841A1.5 1.5 0 004 4.11V15.89a1.5 1.5 0 002.3 1.269l9.344-5.89a1.5 1.5 0 000-2.538L6.3 2.84z"/></svg>
                    </button>
                </div>
                <h3 class="font-bold text-white truncate">${track.title}</h3>
                <p class="text-sm text-gray-400 truncate">${track.artist}</p>
            </div>
            `;
            const el = document.createElement('div');
            el.innerHTML = html;
            el.querySelector('.play-btn').onclick = (e) => { e.stopPropagation(); playTrack(track); };
            el.onclick = () => playTrack(track); // Also play on card click
            container.appendChild(el);

        } else {
            // Render as list rows
            const el = document.createElement('div');
            el.className = 'flex items-center p-3 rounded-md hover:bg-white/10 transition group cursor-pointer';
            el.innerHTML = `
                <div class="w-10 text-zyra-muted group-hover:text-white">${index + 1}</div>
                <div class="flex-1 flex items-center space-x-4">
                    <img src="${track.cover_image || 'https://via.placeholder.com/40'}" class="w-10 h-10 bg-gray-700 object-cover">
                    <div>
                        <div class="font-bold text-white">${track.title}</div>
                        <div class="text-sm text-zyra-muted">${track.artist}</div>
                    </div>
                </div>
                <div class="w-1/3 text-sm text-zyra-muted hidden md:block">${track.album || 'Single'}</div>
                <div class="w-24 text-right pr-4">
                    <button class="like-btn ${heartClass} transition transform active:scale-90" data-id="${track.id}">
                        <svg class="w-5 h-5" fill="${isLiked ? 'currentColor' : 'none'}" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/></svg>
                    </button>
                </div>
                <div class="w-16 text-right text-sm text-zyra-muted">
                    ${track.is_premium ? '<span class="text-xs bg-zyra-accent text-black px-1 rounded font-bold">PREMP</span>' : ''}
                </div>
            `;

            // Interaction handlers
            el.onclick = (e) => {
                if (!e.target.closest('.like-btn')) playTrack(track);
            };

            const likeBtn = el.querySelector('.like-btn');
            likeBtn.onclick = async (e) => {
                e.preventDefault();
                e.stopPropagation();
                await toggleLike(track.id, likeBtn);
            };

            container.appendChild(el);
        }
    });
}

async function toggleLike(musicId, btn) {
    const isLiked = likedSongIds.has(musicId);
    const method = isLiked ? 'DELETE' : 'POST';

    try {
        const res = await fetchWithAuth(`/api/music/${musicId}/like`, { method });
        if (res.ok) {
            if (isLiked) {
                likedSongIds.delete(musicId);
                btn.classList.remove('text-green-500', 'fill-current');
                btn.classList.add('text-gray-400');
                btn.querySelector('svg').setAttribute('fill', 'none');
            } else {
                likedSongIds.add(musicId);
                btn.classList.remove('text-gray-400');
                btn.classList.add('text-green-500', 'fill-current');
                btn.querySelector('svg').setAttribute('fill', 'currentColor');
            }
        }
    } catch (e) { console.error(e); }
}

async function loadPlans() {
    const res = await fetch('/api/plans');
    const plans = await res.json();
    const container = document.getElementById('plans-container');
    container.innerHTML = '';

    plans.forEach(plan => {
        const card = document.createElement('div');
        card.className = 'bg-[#282828] p-6 rounded-lg border border-gray-600 hover:border-zyra-primary transition flex flex-col items-center';
        card.innerHTML = `
            <h3 class="text-2xl font-bold mb-2 text-white">${plan.name}</h3>
            <div class="text-4xl font-bold mb-4 text-zyra-primary">₹${plan.price}</div>
            <p class="text-gray-400 text-sm mb-6">${plan.duration_days} days</p>
            <ul class="text-sm text-gray-300 space-y-2 mb-6">
                ${plan.name === 'Premium' ? '<li>✔️ Ad-free music</li><li>✔️ Offline playback</li>' : '<li>✔️ Shuffle play</li><li>❌ Ad-free music</li>'}
            </ul>
            <button onclick="openPaymentModal(${plan.id}, '${plan.name}', ${plan.price})" class="w-full py-2 bg-white text-black font-bold rounded-full hover:scale-105 transition">
                Get ${plan.name}
            </button>
        `;
        container.appendChild(card);
    });
}

// Payment Logic
let selectedPlanId = null;

function openPaymentModal(id, name, price) {
    selectedPlanId = id;
    document.getElementById('upgrade-modal').classList.add('hidden');
    const paymentModal = document.getElementById('payment-modal');
    paymentModal.classList.remove('hidden');

    document.getElementById('payment-plan-name').textContent = name;
    document.getElementById('payment-plan-price').textContent = `₹${price}`;

    // Close handler
    document.getElementById('close-payment').onclick = () => {
        paymentModal.classList.add('hidden');
    };
}

document.getElementById('payment-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const btn = document.getElementById('pay-btn');
    const originalText = btn.innerHTML;

    // Validate (basic)
    const inputs = e.target.querySelectorAll('input');
    let valid = true;
    inputs.forEach(i => {
        if (!i.value) { i.classList.add('border-red-500'); valid = false; }
        else i.classList.remove('border-red-500');
    });
    if (!valid) return;

    // Simulate Processing
    btn.disabled = true;
    btn.innerHTML = `<svg class="animate-spin h-5 w-5 text-white mr-2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg> Processing...`;

    await new Promise(r => setTimeout(r, 2000)); // 2s fake delay

    // Call API
    await subscribe(selectedPlanId);
});

async function subscribe(planId) {
    try {
        const res = await fetchWithAuth('/api/subscribe', {
            method: 'POST',
            body: JSON.stringify({ plan_id: planId })
        });
        const result = await res.json();

        const btn = document.getElementById('pay-btn');
        if (res.ok) {
            btn.innerHTML = `<span>Success!</span>`;
            btn.classList.remove('bg-black');
            btn.classList.add('bg-green-500');

            setTimeout(() => {
                // Update local user data simpler way
                const user = JSON.parse(localStorage.getItem('user'));
                user.subscription = result.subscription;
                localStorage.setItem('user', JSON.stringify(user));
                window.location.reload();
            }, 1000);

        } else {
            alert(result.error);
            btn.disabled = false;
            btn.innerHTML = 'Pay Now';
        }
    } catch (err) {
        alert('Payment failed');
        document.getElementById('pay-btn').disabled = false;
        document.getElementById('pay-btn').innerHTML = 'Pay Now';
    }
}

function playTrack(track) {
    currentTrack = track;

    // UI Updates
    document.getElementById('player-cover').src = track.cover_image || 'https://via.placeholder.com/40';
    document.getElementById('player-cover').classList.remove('hidden');
    document.getElementById('player-info').classList.remove('hidden');
    document.getElementById('player-title').textContent = track.title;
    document.getElementById('player-artist').textContent = track.artist;

    // Audio Player
    audioPlayer.src = track.url;
    audioPlayer.play().catch(e => console.log('Playback error:', e)); // Handle autoplay policies
    isPlaying = true;
    updatePlayButton();
}

async function fetchWithAuth(url, options = {}) {
    const token = localStorage.getItem('access_token');
    const headers = options.headers || {};

    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    if (options.body && typeof options.body === 'string') {
        headers['Content-Type'] = 'application/json';
    }

    const res = await fetch(url, { ...options, headers });

    if (res.status === 401) {
        // Token expired/invalid - simplified for this demo
        localStorage.clear();
        window.location.href = '/login';
    }

    return res;
}

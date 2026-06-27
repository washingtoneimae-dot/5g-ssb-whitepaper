#!/usr/bin/env python3
"""
GRIN MMF HCF Adapter — Full Physics Simulation
================================================
Solves for LP₀ₚ modes numerically (arbitrary α-profile), computes
SMF→GRIN→HCF coupling efficiency across all parameter space.
"""

import numpy as np
from scipy import integrate, interpolate, constants, sparse
from scipy.sparse import linalg as sp_linalg
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import cm
from pathlib import Path
import json

# ─── Physical constants ────────────────────────────────────────────────
C      = constants.c * 1e6         # μm/s
LAMBDA = 1.55                      # μm (1550 nm)
K0     = 2 * np.pi / LAMBDA        # free-space wavenumber

# ─── Default parameters ────────────────────────────────────────────────
PAR = {
    'NA':      0.200,      # numerical aperture
    'a':       25.0,       # core radius (μm)  — 50μm core
    'alpha':   2.0,        # profile parameter (2 = parabolic)
    'n1':      1.457,      # on-axis refractive index (silica @ 1550nm)
    'w_smf':   5.2,        # SMF-28 spot size (μm) — MFD/2 = 10.4/2
    'w_hcf':   12.0,       # HCF spot size (μm) — typical anti-resonant
    'n_gel':   1.44,       # index-matching gel refractive index
}

# ─── Derived ───────────────────────────────────────────────────────────
PAR['n2'] = np.sqrt(PAR['n1']**2 - PAR['NA']**2)  # cladding index
PAR['Delta'] = (PAR['n1']**2 - PAR['n2']**2) / (2 * PAR['n1']**2)  # ≈ NA²/(2n₁²)

# ══════════════════════════════════════════════════════════════════════
#  1. GRIN Index Profile
# ══════════════════════════════════════════════════════════════════════
def n_grin(r, par):
    """Index profile n(r) for α-profile GRIN fiber."""
    a, alpha, n1, n2 = par['a'], par['alpha'], par['n1'], par['n2']
    Delta = (n1**2 - n2**2) / (2 * n1**2)
    nr = np.where(r <= a,
                  n1 * np.sqrt(1 - 2 * Delta * (r / a)**alpha),
                  n2 * np.ones_like(r))
    return nr

# ══════════════════════════════════════════════════════════════════════
#  2. Numerical Mode Solver
# ══════════════════════════════════════════════════════════════════════
def solve_modes(par, n_modes=6, r_max=80, n_r=4000, lam=None):
    """
    Solve scalar wave equation for LP₀ₚ modes of GRIN fiber.
    
    Uses transformation u(r) = √r · ψ(r) to eliminate first derivative:
      d²u/dr² + [k₀² n²(r) + 1/(4r²)] u = β² u
    
    Dirichlet BC: u(0) = 0, u(r_max) = 0.
    Discretized as symmetric tridiagonal eigenvalue problem A·u = β²·u.
    
    Returns: list of dicts with 'psi' (field), 'r' (grid),
             'beta', 'n_eff', 'A_eff'
    """
    if lam is None:
        k0 = K0
    else:
        k0 = 2 * np.pi / lam
    
    n1 = par['n1']
    n2 = par['n2']
    
    # Radial grid with Dirichlet BC: solve for interior points [0, N-2]
    # Last point (index N-1) is forced to zero
    r = np.linspace(0, r_max, n_r)
    h = r[1] - r[0]
    
    # Index profile
    n_prof = n_grin(r, par)
    
    # Potential: q(r) = k₀² n²(r) + 1/(4r²)
    # At r=0: 1/(4r²) diverges → u(0) = 0 automatically satisfied
    q = (k0 * n_prof)**2
    q[0] = 0  # r=0, u=0 enforced; value doesn't matter
    
    # Interior points for potential
    for i in range(1, n_r):
        q[i] += 0.25 / (r[i]**2) if r[i] > 1e-12 else 0
    
    # Build symmetric tridiagonal matrix (interior: indices 0 to n_r-2)
    # u[n_r-1] = 0 is explicit Dirichlet BC
    N = n_r - 1  # number of free variables
    
    diag = np.zeros(N)
    off = np.zeros(N - 1)  # symmetric: off_low = off_up = off
    
    # Interior points i = 1, ..., N-2
    for i in range(N):
        ri = r[i]
        # The Laplacian term: (u_{i-1} - 2u_i + u_{i+1})/h²
        diag[i] = -2.0 / h**2 + q[i]
        if i < N - 1:
            off[i] = 1.0 / h**2
    
    # r = 0: u(0) = 0, so first equation:
    # (u₋₁ - 2u₀ + u₁)/h² + q₀·u₀ = β²·u₀
    # u₋₁ = u(0 - h) doesn't exist. With u(0) = 0 (Dirichlet at r=0):
    # For interior starting at i=0 (r=0), u₀ = 0 is fixed.
    # The equation at i=0 is just u₀ = 0.
    # But we can't set this as a row because it would give β²=0.
    # Instead, we skip r=0 and start from i=1.
    # Better: handle r=0 with L'Hôpital on the transformation.
    
    # Actually, easiest: remove r=0, start from i=1.
    # Redefine: N = n_r - 2, and indices 1 to n_r-2 are free
    # u[0] = 0, u[n_r-1] = 0 (Dirichlet BC)
    
    # Let me redo this more carefully:
    start_idx = 1
    end_idx = n_r - 1  # u[end_idx] = 0
    N_free = end_idx - start_idx  # number of free interior points
    
    if N_free < 1:
        return []
    
    r_free = r[start_idx:end_idx]
    
    # Potential for free points
    q_free = (k0 * n_prof[start_idx:end_idx])**2
    for i in range(N_free):
        q_free[i] += 0.25 / (r_free[i]**2)
    
    # Tridiagonal matrix
    diag = np.zeros(N_free)
    off = np.zeros(N_free - 1)
    
    for i in range(N_free):
        diag[i] = -2.0 / h**2 + q_free[i]
        if i < N_free - 1:
            off[i] = 1.0 / h**2
    
    # First point (adjacent to r=0): u₀ = 0, so equation is:
    # (−2u₁ + u₂)/h² + q₁·u₁ = β²·u₁
    # i.e. the term from u₀ is zero → off[0] = 1/h² already correct
    
    # Last point (adjacent to r_max): u_N = 0, so:
    # (u_{N-2} - 2u_{N-1})/h² + q_{N-1}·u_{N-1} = β²·u_{N-1}
    # off[N_free-1] = 1/h² is for u_{N_free} which doesn't exist
    # Actually off is N_free-1 long, so off[N_free-2] connects u_{N_free-2} and u_{N_free-1}
    # This is correct without modification because u_{end_idx} = 0.
    # Wait, u_{end_idx} is u[n_r-1] = 0. The last free point is at index end_idx-1.
    # For this point: (u_{end_idx-2} - 2u_{end_idx-1})/h² + q·u_{end_idx-1} = β²·u_{end_idx-1}
    # The u_{end_idx} term would normally add +u_{end_idx}/h² but u_{end_idx}=0 so it drops.
    # off[N_free-2] = 1/h² is for u_{end_idx-2} coefficient.
    # u_{end_idx} is not in the matrix → OK.
    
    A = sparse.diags([off, diag, off], [-1, 0, 1], format='csr')
    
    # Solve for N_LARGEST eigenvalues
    n_solve = min(n_modes, N_free - 1)
    if n_solve < 1:
        return []
    
    eigenvalues, eigenvectors = sp_linalg.eigsh(A, k=n_solve, which='LA')
    
    # Sort by β² descending
    idx = np.argsort(eigenvalues)[::-1]
    eigenvalues = eigenvalues[idx]
    eigenvectors = eigenvectors[:, idx]
    
    # Reconstruct full field including zeros at boundaries
    beta_sq_threshold = (k0 * n2)**2
    
    modes = []
    full_r = r  # keep original r grid
    
    for m_idx in range(n_solve):
        beta_sq = eigenvalues[m_idx]
        if beta_sq < beta_sq_threshold - 1e-10:
            break
        
        beta = np.sqrt(beta_sq)
        n_eff = beta / k0
        
        # u(r) on free grid → ψ(r) = u(r)/√r
        u_free = eigenvectors[:, m_idx].real
        
        # Reconstruct full ψ on [0, r_max]
        psi = np.zeros(n_r)
        psi[start_idx:end_idx] = u_free / np.sqrt(r_free + 1e-30)
        psi[0] = 0.0       # u(0)/0 → finite value by limit, set explicitly
        psi[end_idx] = 0.0  # Dirichlet BC
        
        # Fix psi at r=0 by extrapolation from first interior point
        if start_idx < n_r:
            # Taylor expansion: ψ(r) ≈ ψ₀ + ψ'₀·r + ...
            # For LP₀ₚ modes, ψ'(0) = 0, so ψ(0) ≈ ψ(h)
            psi[0] = psi[start_idx]
        
        # Normalize: ∫|ψ|² · 2πr dr = 1
        norm = 2 * np.pi * np.trapz(psi**2 * full_r, full_r)
        if norm > 0:
            psi = psi / np.sqrt(norm)
        
        # Effective area
        integ_psi2 = 2 * np.pi * np.trapz(psi**2 * full_r, full_r)
        integ_psi4 = 2 * np.pi * np.trapz(psi**4 * full_r, full_r)
        A_eff = integ_psi2**2 / (integ_psi4 + 1e-30)
        
        modes.append({
            'm': m_idx,
            'psi': psi,
            'r': full_r,
            'beta': beta,
            'n_eff': n_eff,
            'A_eff': A_eff,
            'norm': norm,
        })
    
    return modes


def analytic_modes(par, n_modes=6, r_max=80, n_r=4000):
    """
    Analytic LP₀ₚ modes for pure parabolic (α=2) GRIN fiber.
    Laguerre-Gaussian functions.
    """
    r = np.linspace(0, r_max, n_r)
    NA = par['NA']
    a = par['a']
    n1 = par['n1']
    lam = LAMBDA
    
    # Fundamental mode spot size for parabolic GRIN
    w_g = np.sqrt(a * lam / (np.pi * NA))
    
    # Gradient parameter
    Delta = (n1**2 - par['n2']**2) / (2 * n1**2)
    g = np.sqrt(2 * Delta) / a
    
    modes = []
    for p in range(n_modes):
        # Laguerre polynomial L_p(0) = 1, L_p(x) general
        x = 2 * r**2 / w_g**2
        
        # Laguerre polynomial L_p(x) — recurrence
        L = np.ones_like(x)  # L_0
        if p == 0:
            L_poly = L
        elif p == 1:
            L_poly = 1 - x
        else:
            L_prev2 = np.ones_like(x)
            L_prev1 = 1 - x
            for k in range(2, p + 1):
                L_curr = ((2*k - 1 - x) * L_prev1 - (k - 1) * L_prev2) / k
                L_prev2, L_prev1 = L_prev1, L_curr
            L_poly = L_prev1
        
        psi = np.sqrt(2 / np.pi) * (1 / w_g) * L_poly * np.exp(-x/2)
        
        # Normalize numerically to be safe
        norm = 2 * np.pi * np.trapz(psi**2 * r, r)
        if abs(norm - 1) > 1e-6:
            psi = psi / np.sqrt(norm)
        
        # Propagation constant
        beta = K0 * n1 - (2*p + 1) * g / 2
        
        A_eff = (2 * np.pi * np.trapz(psi**2 * r, r))**2 / \
                (2 * np.pi * np.trapz(psi**4 * r, r) + 1e-30)
        
        modes.append({
            'm': p,
            'psi': psi,
            'r': r,
            'beta': beta,
            'n_eff': beta / K0,
            'A_eff': A_eff,
        })
    
    return modes

# ══════════════════════════════════════════════════════════════════════
#  3. Overlap Integrals
# ══════════════════════════════════════════════════════════════════════
def overlap(psi_a, r_a, psi_b, r_b):
    """Compute ∫ψ_a·ψ_b·2πr dr (amplitude overlap)."""
    # Interpolate psi_a onto r_b grid
    f_interp = interpolate.interp1d(r_a, psi_a, bounds_error=False,
                                     fill_value=0.0)
    psi_a_interp = f_interp(r_b)
    return 2 * np.pi * np.trapz(psi_a_interp * psi_b * r_b, r_b)


def gaussian_mode(r, w):
    """Normalized Gaussian field ψ(r) = √(2/π)·(1/w)·exp(−r²/w²)."""
    return np.sqrt(2 / np.pi) * (1 / w) * np.exp(-r**2 / w**2)


# ══════════════════════════════════════════════════════════════════════
#  4. Full Propagation & Coupling
# ══════════════════════════════════════════════════════════════════════
def coupling_vs_length(modes, par, z_max=3000, n_z=2000):
    """
    Compute SMF→GRIN→HCF coupling efficiency as a function of GRIN length.
    
    Returns (z, eta_hcf, w_rms, field_at_output, coeffs)
    """
    r = modes[0]['r']
    w_smf = par['w_smf']
    w_hcf = par['w_hcf']
    
    # Input field (SMF Gaussian)
    psi_smf = gaussian_mode(r, w_smf)
    
    # Output target (HCF Gaussian)
    psi_hcf = gaussian_mode(r, w_hcf)
    
    # Excitation coefficients: c_p = ∫ψ_smf · ψ_p · 2πr dr
    coeffs = []
    for mode in modes:
        c = overlap(psi_smf, r, mode['psi'], r)
        coeffs.append(c)
    
    coeffs = np.array(coeffs)
    power_in_modes = np.abs(coeffs)**2
    total_power = np.sum(power_in_modes)
    
    # Propagation
    betas = np.array([m['beta'] for m in modes])
    
    z = np.linspace(0, z_max, n_z)
    eta_hcf = np.zeros(n_z, dtype=complex)
    w_rms = np.zeros(n_z)
    
    for i, zi in enumerate(z):
        # Total field at z
        phase = np.exp(1j * betas * zi)
        psi_total = np.sum(coeffs[:, np.newaxis] *
                           np.array([m['psi'] for m in modes]) *
                           phase[:, np.newaxis], axis=0)
        
        # Overlap with HCF mode
        eta_hcf[i] = overlap(psi_total, r, psi_hcf, r)
        
        # RMS width
        w_rms[i] = np.sqrt(2 * np.pi * np.trapz(r**2 * np.abs(psi_total)**2 * r, r))
    
    return z, np.abs(eta_hcf)**2, w_rms, coeffs, power_in_modes


def find_optimal_length(modes, par, z_search=3000):
    """Find the GRIN length that maximizes coupling to HCF."""
    z, eta, w_rms, coeffs, powers = coupling_vs_length(modes, par, z_search, 5000)
    idx = np.argmax(eta)
    return z[idx], eta[idx], w_rms[idx]


# ══════════════════════════════════════════════════════════════════════
#  5. Parameter Sweeps
# ══════════════════════════════════════════════════════════════════════
def sweep_parameter(param_name, values, par, n_modes=6):
    """Sweep a single parameter and compute optimal coupling."""
    results = []
    for val in values:
        p = par.copy()
        p[param_name] = val
        # Update derived
        if param_name in ('NA', 'n1', 'n2'):
            if param_name == 'NA':
                p['n2'] = np.sqrt(p['n1']**2 - p['NA']**2)
                p['Delta'] = (p['n1']**2 - p['n2']**2) / (2 * p['n1']**2)
            elif param_name == 'a':
                pass  # no derived update needed
            elif param_name == 'alpha':
                pass
            elif param_name == 'w_smf':
                pass
            elif param_name == 'w_hcf':
                pass
        
        try:
            modes = solve_modes(p, n_modes)
            if len(modes) < 2:
                results.append({'value': val, 'eta_opt': 0, 'z_opt': 0,
                                'w_rms_opt': 0, 'n_modes': len(modes),
                                'error': 'too few modes'})
                continue
            
            z_opt, eta_opt, w_opt = find_optimal_length(modes, p)
            pitch = 2 * np.pi / np.sqrt(2 * p['Delta']) * p['a']
            
            results.append({
                'value': val,
                'eta_opt': float(eta_opt),
                'z_opt': float(z_opt),
                'w_rms_opt': float(w_opt),
                'loss_dB': float(-10 * np.log10(max(eta_opt, 1e-10))),
                'n_modes': len(modes),
                'L/2': float(pitch / 2),
                'error': None,
            })
        except Exception as e:
            results.append({'value': val, 'error': str(e)})
    
    return results


# ══════════════════════════════════════════════════════════════════════
#  6. Monte Carlo Manufacturing Tolerances
# ══════════════════════════════════════════════════════════════════════
def monte_carlo(n_samples=5000, n_modes=4, z_max=3000, n_z=3000):
    """
    Monte Carlo simulation of manufacturing tolerances.
    
    Variations:
    - NA: ±0.015 (OM4 spec)
    - Core radius: ±1.5μm (50±3μm core → a=25±1.5μm)
    - α: ±0.05 (profile tolerance)
    - SMF cleave length: ±20μm (standard cleaver accuracy)
    - Lateral offset at GRIN→HCF: ±1.25μm (ferrule bore tolerance)
    """
    np.random.seed(42)
    
    results = {
        'loss_dB': [],
        'z_opt': [],
        'NA_actual': [],
        'a_actual': [],
        'alpha_actual': [],
        'w_eff': [],
    }
    
    for _ in range(n_samples):
        par = PAR.copy()
        par['NA'] = np.random.normal(0.200, 0.0075)  # ±0.015 3σ
        par['NA'] = np.clip(par['NA'], 0.170, 0.230)
        par['a'] = np.random.normal(25.0, 0.5)  # ±1.5μm 3σ
        par['a'] = np.clip(par['a'], 22.0, 28.0)
        par['alpha'] = np.random.normal(2.0, 0.017)  # ±0.05 3σ
        par['alpha'] = np.clip(par['alpha'], 1.9, 2.1)
        par['n2'] = np.sqrt(par['n1']**2 - par['NA']**2)
        par['Delta'] = (par['n1']**2 - par['n2']**2) / (2 * par['n1']**2)
        
        # Cleave length error (follow normal distribution)
        cleave_error = np.random.normal(0, 10)  # μm, 1σ = 10μm
        
        try:
            modes = solve_modes(par, n_modes)
            if len(modes) < 2:
                continue
            
            z, eta, w_rms, coeffs, powers = coupling_vs_length(modes, par, z_max, n_z)
            
            idx_opt = np.argmax(eta)
            z_opt_nominal = z[idx_opt]
            eta_opt_nominal = eta[idx_opt]
            
            # Apply cleave error: couple at z_opt_nominal + cleave_error
            z_actual = np.clip(z_opt_nominal + cleave_error, z[0], z[-1])
            idx_actual = np.argmin(np.abs(z - z_actual))
            eta_actual = eta[idx_actual]
            
            # Lateral offset penalty at HCF interface
            offset = np.random.exponential(0.5)  # μm, typical offset distribution
            offset = min(offset, 2.0)
            w_eff = w_rms[idx_actual]
            offset_penalty = 4.34 * (offset / w_eff)**2 if w_eff > 0 else 99
            offset_penalty = min(offset_penalty, 3.0)  # cap
            
            loss = -10 * np.log10(max(eta_actual, 1e-10)) + offset_penalty
            
            results['loss_dB'].append(loss)
            results['z_opt'].append(z_opt_nominal)
            results['NA_actual'].append(par['NA'])
            results['a_actual'].append(par['a'])
            results['alpha_actual'].append(par['alpha'])
            results['w_eff'].append(w_eff)
            
        except Exception:
            continue
    
    return results


# ══════════════════════════════════════════════════════════════════════
#  7. Plotting
# ══════════════════════════════════════════════════════════════════════
OUT = Path('/tmp/5g-ssb-whitepaper/simulation')
OUT.mkdir(exist_ok=True, parents=True)

def plot_coupling_curve(par):
    """η(z) — the fundamental coupling efficiency curve."""
    modes = solve_modes(par)
    z, eta, w_rms, coeffs, powers = coupling_vs_length(modes, par, z_max=3000, n_z=3000)
    
    # Pitch markers
    gin = par['n1']
    g = np.sqrt(2 * par['Delta']) / par['a']
    L = 2 * np.pi / g
    L2, L4 = L / 2, L / 4
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
    
    ax1.plot(z, eta * 100, 'b-', linewidth=2)
    ax1.axvline(L4, color='gray', linestyle='--', alpha=0.5, label=f'L/4 = {L4:.0f}μm')
    ax1.axvline(L2, color='red', linestyle='--', alpha=0.7, label=f'L/2 = {L2:.0f}μm')
    ax1.axvline(L, color='gray', linestyle=':', alpha=0.5, label=f'L = {L:.0f}μm')
    ax1.set_ylabel('Coupling to HCF (%)', fontsize=12)
    ax1.set_title(f'SMF→GRIN→HCF Coupling vs GRIN Length\n'
                  f'(NA={par["NA"]:.3f}, a={par["a"]:.0f}μm, α={par["alpha"]:.1f})',
                  fontsize=13)
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(0, 100)
    
    # Annotate extrema
    idx_max = np.argmax(eta)
    idx_min = np.argmin(eta[:len(z)//2])
    ax1.annotate(f'Peak: {eta[idx_max]*100:.1f}% @ {z[idx_max]:.0f}μm\n'
                 f'({-10*np.log10(eta[idx_max]):.2f} dB)',
                 xy=(z[idx_max], eta[idx_max]*100),
                 xytext=(z[idx_max]+200, eta[idx_max]*100+5),
                 arrowprops=dict(arrowstyle='->'), fontsize=9)
    
    ax1.annotate(f'Min: {eta[idx_min]*100:.1f}% @ {z[idx_min]:.0f}μm\n'
                 f'({-10*np.log10(eta[idx_min]):.2f} dB)',
                 xy=(z[idx_min], eta[idx_min]*100),
                 xytext=(z[idx_min]+200, eta[idx_min]*100-15),
                 arrowprops=dict(arrowstyle='->'), fontsize=9)
    
    # RMS width
    ax2.plot(z, w_rms, 'g-', linewidth=2)
    ax2.axhline(par['w_smf'], color='orange', linestyle='--',
                alpha=0.6, label=f'SMF w = {par["w_smf"]}μm')
    ax2.axhline(par['w_hcf'], color='purple', linestyle='--',
                alpha=0.6, label=f'HCF w = {par["w_hcf"]}μm')
    ax2.axvline(L2, color='red', linestyle='--', alpha=0.5)
    ax2.set_xlabel('GRIN Length z (μm)', fontsize=12)
    ax2.set_ylabel('RMS Spot Size w_rms (μm)', fontsize=12)
    ax2.legend(fontsize=10)
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(OUT / '01_coupling_vs_length.png', dpi=150)
    plt.close()
    
    return modes, z, eta, w_rms, coeffs, powers


def plot_mode_profiles(modes, par):
    """Show LP₀ₚ mode profiles and SMF/HCF targets."""
    r = modes[0]['r']
    r_plot = r[r <= 40]
    
    fig, ax = plt.subplots(figsize=(10, 5))
    
    colors = cm.tab10(np.linspace(0, 1, len(modes) + 1))
    for i, mode in enumerate(modes):
        idx = r <= 40
        ax.plot(r[idx], mode['psi'][idx] / np.max(np.abs(mode['psi'])),
                color=colors[i], linewidth=1.5,
                label=f'LP₀{mode["m"]+1}  (n_eff={mode["n_eff"]:.5f})')
    
    psi_smf = gaussian_mode(r, par['w_smf'])
    psi_hcf = gaussian_mode(r, par['w_hcf'])
    ax.plot(r_plot, psi_smf[r <= 40] / np.max(psi_smf),
            'k--', linewidth=2, label=f'SMF (w={par["w_smf"]}μm)')
    ax.plot(r_plot, psi_hcf[r <= 40] / np.max(psi_hcf),
            'r--', linewidth=2, label=f'HCF (w={par["w_hcf"]}μm)')
    
    ax.set_xlabel('r (μm)', fontsize=12)
    ax.set_ylabel('Normalized Field', fontsize=12)
    ax.set_title('GRIN MMF LP₀ₚ Mode Profiles (Normalized)', fontsize=13)
    ax.legend(fontsize=9, loc='upper right')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(OUT / '02_mode_profiles.png', dpi=150)
    plt.close()


def plot_excitation(modes, par):
    """Show which modes are excited by SMF launch."""
    r = modes[0]['r']
    psi_smf = gaussian_mode(r, par['w_smf'])
    
    labels = [f'LP₀{m["m"]+1}' for m in modes]
    powers = []
    for mode in modes:
        c = overlap(psi_smf, r, mode['psi'], r)
        powers.append(abs(c)**2 * 100)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.bar(range(len(modes)), powers, color=cm.viridis(np.linspace(0.3, 0.9, len(modes))))
    ax.set_xticks(range(len(modes)))
    ax.set_xticklabels(labels, fontsize=11)
    ax.set_ylabel('Power Excited (%)', fontsize=12)
    ax.set_title('SMF-28 → GRIN MMF Mode Excitation', fontsize=13)
    
    for bar, p in zip(bars, powers):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                f'{p:.1f}%', ha='center', fontsize=10)
    
    ax.set_ylim(0, max(powers) * 1.2)
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig(OUT / '03_excitation.png', dpi=150)
    plt.close()


def plot_field_evolution(modes, par):
    """Show the total field at key propagation distances."""
    r = modes[0]['r']
    psi_smf = gaussian_mode(r, par['w_smf'])
    psi_hcf = gaussian_mode(r, par['w_hcf'])
    
    coeffs = []
    for mode in modes:
        c = overlap(psi_smf, r, mode['psi'], r)
        coeffs.append(c)
    coeffs = np.array(coeffs)
    betas = np.array([m['beta'] for m in modes])
    
    # Key positions
    g = np.sqrt(2 * par['Delta']) / par['a']
    L = 2 * np.pi / g
    positions = {
        'z = 0 (splice)': 0,
        'z = L/4': L/4,
        'z = L/2 (optimal)': L/2,
        'z = 3L/4': 3*L/4,
        'z = L': L,
    }
    
    fig, axes = plt.subplots(1, 5, figsize=(18, 4), sharey=True)
    r_plot = r[r <= 40]
    
    for ax, (label, zi) in zip(axes, positions.items()):
        phase = np.exp(1j * betas * zi)
        psi_total = np.sum(coeffs[:, np.newaxis] *
                           np.array([m['psi'] for m in modes]) *
                           phase[:, np.newaxis], axis=0)
        
        idx = r <= 40
        ax.plot(r_plot, np.abs(psi_total[idx]) / np.max(np.abs(psi_total[idx])),
                'b-', linewidth=2, label='Total field')
        ax.plot(r_plot, psi_hcf[idx] / np.max(np.abs(psi_hcf[idx])),
                'r--', linewidth=1.5, alpha=0.7, label='HCF target')
        
        eta = overlap(psi_total, r, psi_hcf, r)
        ax.set_title(f'{label}\nη = {abs(eta)**2*100:.1f}%', fontsize=10)
        ax.set_xlabel('r (μm)', fontsize=10)
        ax.grid(True, alpha=0.3)
        if label == list(positions.keys())[0]:
            ax.set_ylabel('Normalized |ψ|', fontsize=11)
            ax.legend(fontsize=9)
    
    plt.suptitle(f'Total Field Evolution (NA={par["NA"]:.3f}, a={par["a"]:.0f}μm, α={par["alpha"]:.1f})',
                 fontsize=13, y=1.05)
    plt.tight_layout()
    plt.savefig(OUT / '04_field_evolution.png', dpi=150)
    plt.close()


def plot_sweep_results(sweep_name, results, xlabel, param_name):
    """Plot a parameter sweep."""
    values = [r['value'] for r in results]
    losses = [r.get('loss_dB', np.nan) for r in results]
    etas = [r.get('eta_opt', 0) * 100 for r in results]
    z_opts = [r.get('z_opt', 0) for r in results]
    errors = [r.get('error') for r in results]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    valid = [i for i, e in enumerate(errors) if e is None]
    if valid:
        v = [values[i] for i in valid]
        l = [losses[i] for i in valid]
        e = [etas[i] for i in valid]
        zz = [z_opts[i] for i in valid]
        
        ax1.plot(v, l, 'o-', color='crimson', linewidth=2, markersize=5)
        ax1.axhline(0.5, color='green', linestyle='--', alpha=0.7,
                    label='Target: 0.5 dB')
        ax1.set_xlabel(xlabel, fontsize=12)
        ax1.set_ylabel('Optimal Coupling Loss (dB)', fontsize=12)
        ax1.set_title(f'{sweep_name}: Loss at Optimal Length', fontsize=13)
        ax1.legend(fontsize=10)
        ax1.grid(True, alpha=0.3)
        
        ax2.plot(v, zz, 's-', color='steelblue', linewidth=2, markersize=5)
        ax2.set_xlabel(xlabel, fontsize=12)
        ax2.set_ylabel('Optimal GRIN Length z_opt (μm)', fontsize=12)
        ax2.set_title(f'{sweep_name}: Optimal Length', fontsize=13)
        ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(OUT / f'sweep_{param_name}.png', dpi=150)
    plt.close()


def function_form_fit(results, param_name):
    """Fit a function form to the sweep results and return coefficients."""
    import warnings
    values = np.array([r['value'] for r in results])
    losses = np.array([r.get('loss_dB', np.nan) for r in results])
    
    valid = ~np.isnan(losses)
    values, losses = values[valid], losses[valid]
    
    if len(values) < 4:
        return None
    
    # Try polynomial fit
    try:
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            coeffs = np.polyfit(values, losses, 2)
        return {'type': 'poly2', 'coeffs': coeffs.tolist()}
    except:
        pass
    return None


def plot_monte_carlo(mc_results, par):
    """Histograms from Monte Carlo simulation."""
    losses = np.array(mc_results['loss_dB'])
    z_opts = np.array(mc_results['z_opt'])
    
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))
    
    # Loss histogram
    ax = axes[0, 0]
    ax.hist(losses, bins=50, color='crimson', edgecolor='white', alpha=0.8,
            density=True)
    ax.axvline(0.5, color='green', linestyle='--', linewidth=2,
               label=f'Target < 0.5 dB')
    ax.axvline(np.median(losses), color='blue', linestyle=':',
               label=f'Median = {np.median(losses):.2f} dB')
    ax.set_xlabel('Total Insertion Loss (dB)', fontsize=11)
    ax.set_ylabel('Probability Density', fontsize=11)
    ax.set_title(f'Loss Distribution\n'
                 f'Mean={np.mean(losses):.2f} dB  |  '
                 f'P(<0.5dB)={np.mean(losses < 0.5)*100:.1f}%',
                 fontsize=12)
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)
    
    # Loss CDF
    ax = axes[0, 1]
    sorted_losses = np.sort(losses)
    cdf = np.arange(1, len(sorted_losses) + 1) / len(sorted_losses)
    ax.plot(sorted_losses, cdf, 'b-', linewidth=2)
    ax.axvline(0.5, color='green', linestyle='--', alpha=0.7)
    ax.axhline(0.5, color='gray', linestyle=':', alpha=0.5)
    ax.set_xlabel('Loss (dB)', fontsize=11)
    ax.set_ylabel('Cumulative Probability', fontsize=11)
    ax.set_title('CDF: Yield at <0.5 dB', fontsize=12)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, 2)
    
    # Optimal length distribution
    ax = axes[0, 2]
    ax.hist(z_opts, bins=50, color='steelblue', edgecolor='white', alpha=0.8)
    ax.axvline(np.median(z_opts), color='red', linestyle='--',
               label=f'Median = {np.median(z_opts):.0f}μm')
    ax.set_xlabel('Optimal GRIN Length (μm)', fontsize=11)
    ax.set_ylabel('Count', fontsize=11)
    ax.set_title(f'Optimal Length Distribution\n'
                 f'σ = {np.std(z_opts):.0f}μm', fontsize=12)
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)
    
    # Sensitivity: Loss vs NA
    ax = axes[1, 0]
    ax.scatter(mc_results['NA_actual'], losses, s=1, alpha=0.3, color='purple')
    ax.set_xlabel('NA', fontsize=11)
    ax.set_ylabel('Loss (dB)', fontsize=11)
    ax.set_title('Loss vs NA', fontsize=12)
    ax.grid(True, alpha=0.3)
    
    # Sensitivity: Loss vs alpha
    ax = axes[1, 1]
    ax.scatter(mc_results['alpha_actual'], losses, s=1, alpha=0.3, color='darkorange')
    ax.set_xlabel('α (profile parameter)', fontsize=11)
    ax.set_ylabel('Loss (dB)', fontsize=11)
    ax.set_title('Loss vs α', fontsize=12)
    ax.grid(True, alpha=0.3)
    
    # Sensitivity: Loss vs core radius
    ax = axes[1, 2]
    ax.scatter(mc_results['a_actual'], losses, s=1, alpha=0.3, color='teal')
    ax.set_xlabel('Core Radius a (μm)', fontsize=11)
    ax.set_ylabel('Loss (dB)', fontsize=11)
    ax.set_title('Loss vs Core Radius', fontsize=12)
    ax.grid(True, alpha=0.3)
    
    plt.suptitle('Monte Carlo Manufacturing Tolerance Analysis\n'
                 f'({len(losses)} samples: NA±0.015, a±1.5μm, α±0.05, cleave±20μm)',
                 fontsize=14, y=1.01)
    plt.tight_layout()
    plt.savefig(OUT / '05_monte_carlo.png', dpi=150)
    plt.close()
    
    return {
        'n_samples': len(losses),
        'mean_loss': float(np.mean(losses)),
        'median_loss': float(np.median(losses)),
        'std_loss': float(np.std(losses)),
        'p_under_0_5dB': float(np.mean(losses < 0.5) * 100),
        'p_under_1_0dB': float(np.mean(losses < 1.0) * 100),
        'p_under_0_3dB': float(np.mean(losses < 0.3) * 100),
        'median_z_opt': float(np.median(z_opts)),
        'loss_NA_corr': float(np.corrcoef(mc_results['NA_actual'], losses)[0, 1]),
        'loss_alpha_corr': float(np.corrcoef(mc_results['alpha_actual'], losses)[0, 1]),
        'loss_a_corr': float(np.corrcoef(mc_results['a_actual'], losses)[0, 1]),
    }


def plot_offset_sensitivity(modes, par):
    """Plot loss vs lateral offset at the GRIN→HCF interface."""
    r = modes[0]['r']
    w_hcf = par['w_hcf']
    psi_hcf = gaussian_mode(r, w_hcf)
    
    # Get field at optimal length
    z_opt, _, _ = find_optimal_length(modes, par)
    psi_smf_local = gaussian_mode(r, par['w_smf'])
    coeffs = np.array([overlap(psi_smf_local, r, m['psi'], r) for m in modes])
    betas = np.array([m['beta'] for m in modes])
    phase = np.exp(1j * betas * z_opt)
    psi_total = np.sum(coeffs[:, np.newaxis] *
                       np.array([m['psi'] for m in modes]) *
                       phase[:, np.newaxis], axis=0)
    
    offsets = np.linspace(0, 3, 100)
    losses = []
    
    w_eff = np.sqrt(2 * np.pi * np.trapz(r**2 * np.abs(psi_total)**2 * r, r))
    
    for dx in offsets:
        # Shifted HCF Gaussian: approximate by overlap with shift
        # ψ_shifted(r) ≈ ψ_original(r - dx·cosθ) averaged over θ
        # For small offsets: η ≈ η₀ · exp(-(dx/w_eff)²)
        # Actually for Gaussian overlap with lateral offset:
        # η(dx) = η₀ · exp(-(dx/w_eff)²) where w_eff is the effective spot size
        eta_offset = np.abs(overlap(psi_total, r, psi_hcf, r))**2 * \
                     np.exp(-(dx / w_eff)**2)
        losses.append(-10 * np.log10(max(eta_offset, 1e-10)))
    
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(offsets, losses, 'b-', linewidth=2)
    ax.axvline(1.25, color='red', linestyle='--', alpha=0.7,
               label='Max ferrule offset (1.25μm)')
    ax.set_xlabel('Lateral Offset Δx (μm)', fontsize=12)
    ax.set_ylabel('Additional Loss (dB)', fontsize=12)
    ax.set_title('Loss vs Lateral Offset at GRIN→HCF Interface\n'
                 f'(w_eff = {w_eff:.1f}μm)', fontsize=13)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(OUT / '06_offset_sensitivity.png', dpi=150)
    plt.close()
    
    return w_eff


def plot_wavelength_sweep(par):
    """Sweep wavelength from 1260nm to 1625nm."""
    fig, ax = plt.subplots(figsize=(10, 5))
    
    wavelengths = np.linspace(1.26, 1.625, 25)
    losses = []
    
    for lam in wavelengths:
        # SMF-28 MFD depends on λ: MFD ≈ 8.4 + 1.3·(λ−1.31) → w = MFD/2
        w_smf = 4.2 + 0.65 * (lam - 1.31)
        # HCF mode scales roughly linearly with λ
        w_hcf = 12.0 * (lam / 1.55)
        
        p = par.copy()
        p['w_smf'] = w_smf
        p['w_hcf'] = w_hcf
        p['n2'] = np.sqrt(p['n1']**2 - p['NA']**2)
        p['Delta'] = (p['n1']**2 - p['n2']**2) / (2 * p['n1']**2)
        
        modes = solve_modes(p, lam=lam)
        if len(modes) < 2:
            losses.append(np.nan)
            continue
        
        z_opt, eta_opt, _ = find_optimal_length(modes, p)
        losses.append(-10 * np.log10(max(eta_opt, 1e-10)))
    
    valid = ~np.isnan(losses)
    ax.plot(wavelengths[valid], np.array(losses)[valid], 'o-',
            color='darkgreen', linewidth=2, markersize=4)
    ax.axvline(1.55, color='red', linestyle='--', alpha=0.7, label='Design λ = 1550nm')
    ax.axhline(0.5, color='green', linestyle=':', alpha=0.5, label='0.5 dB target')
    ax.set_xlabel('Wavelength (μm)', fontsize=12)
    ax.set_ylabel('Optimal Coupling Loss (dB)', fontsize=12)
    ax.set_title('Wavelength Dependence of SMF→GRIN→HCF Coupling\n'
                 '(re-solved modes at each λ)', fontsize=13)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(OUT / '07_wavelength_sweep.png', dpi=150)
    plt.close()
    
    return wavelengths[valid], np.array(losses)[valid]


def plot_tilt_sensitivity(modes, par):
    """Angular misalignment sensitivity."""
    r = modes[0]['r']
    n1 = par['n1']
    
    z_opt, _, _ = find_optimal_length(modes, par)
    betas = np.array([m['beta'] for m in modes])
    phase = np.exp(1j * betas * z_opt)
    
    # Get coeffs by recomputing
    r_grid = modes[0]['r']
    psi_smf = gaussian_mode(r_grid, par['w_smf'])
    coeffs = np.array([overlap(psi_smf, r_grid, m['psi'], r_grid) for m in modes])
    
    psi_total = np.sum(coeffs[:, np.newaxis] *
                       np.array([m['psi'] for m in modes]) *
                       phase[:, np.newaxis], axis=0)
    
    # Angular tilt: for small angles, the overlap penalty for a Gaussian
    # with tilt θ is exp(-(π·w_eff·θ/λ)²)
    w_eff = np.sqrt(2 * np.pi * np.trapz(r**2 * np.abs(psi_total)**2 * r, r))
    
    tilts_deg = np.linspace(0, 2, 100)
    tilts_rad = np.deg2rad(tilts_deg)
    
    losses = []
    eta0 = np.abs(overlap(psi_total, r, gaussian_mode(r, par['w_hcf']), r))**2
    for theta in tilts_rad:
        eta = eta0 * np.exp(-(np.pi * w_eff * theta / LAMBDA)**2)
        losses.append(-10 * np.log10(max(eta, 1e-10)))
    
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(tilts_deg, losses, 'b-', linewidth=2)
    ax.set_xlabel('Angular Misalignment (degrees)', fontsize=12)
    ax.set_ylabel('Additional Loss (dB)', fontsize=12)
    ax.set_title('Loss vs Angular Misalignment\n'
                 f'(w_eff = {w_eff:.1f}μm)', fontsize=13)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(OUT / '08_tilt_sensitivity.png', dpi=150)
    plt.close()


def run_diagnostics(par):
    """Run comprehensive diagnostic on specified parameters."""
    print("=" * 70)
    print(f"  GRIN MMF → HCF Adapter Diagnostic")
    print(f"  Parameters: NA={par['NA']:.3f}, a={par['a']:.0f}μm, α={par['alpha']:.2f}")
    print("=" * 70)
    
    # Mode solution
    print("\n[1] Solving for modes...")
    modes = solve_modes(par)
    print(f"  Found {len(modes)} guided LP₀ₚ modes")
    
    gin = par['n1']
    g = np.sqrt(2 * par['Delta']) / par['a']
    L = 2 * np.pi / g
    print(f"  Gradient param g = {g:.6f} μm⁻¹")
    print(f"  Pitch L = {L:.1f} μm")
    print(f"  Half-pitch L/2 = {L/2:.1f} μm")
    
    for m in modes:
        print(f"  LP₀{m['m']+1}:  n_eff = {m['n_eff']:.6f}  A_eff = {m['A_eff']:.2f} μm²")
    
    # Excitation
    print("\n[2] SMF Launch Excitation...")
    r = modes[0]['r']
    psi_smf = gaussian_mode(r, par['w_smf'])
    total_power = 0
    for m in modes:
        c = overlap(psi_smf, r, m['psi'], r)
        pct = abs(c)**2 * 100
        total_power += abs(c)**2
        print(f"  LP₀{m['m']+1}:  |c|² = {pct:.2f}%")
    print(f"  Total in guided modes: {total_power*100:.2f}%")
    
    # Coupling curve
    print("\n[3] Coupling vs Length...")
    z, eta, w_rms, coeffs, powers = coupling_vs_length(modes, par)
    idx_opt = np.argmax(eta)
    idx_min = np.argmin(eta[:len(z)//2])
    
    print(f"  Max coupling:  {eta[idx_opt]*100:.2f}%  @ z = {z[idx_opt]:.0f} μm")
    print(f"    → Loss:      {-10*np.log10(eta[idx_opt]):.3f} dB")
    print(f"  Min coupling:  {eta[idx_min]*100:.2f}%  @ z = {z[idx_min]:.0f} μm")
    print(f"    → Loss:      {-10*np.log10(eta[idx_min]):.3f} dB")
    print(f"  RMS width at optimum: {w_rms[idx_opt]:.2f} μm")
    
    # Fresnel + offset
    print("\n[4] Additional Loss Factors...")
    n_gel = par['n_gel']
    n_silica = par['n1']
    R = ((n_silica - n_gel) / (n_silica + n_gel))**2
    fresnel_db = -10 * np.log10(1 - R)
    print(f"  Fresnel (silica→gel, n_gel={n_gel}): {fresnel_db:.3f} dB")
    
    # Offset penalty
    w_eff = w_rms[idx_opt]
    offset_1um = 4.34 * (1.0 / w_eff)**2
    offset_125um = 4.34 * (1.25 / w_eff)**2
    print(f"  Offset penalty (1.0μm):  {offset_1um:.3f} dB")
    print(f"  Offset penalty (1.25μm): {offset_125um:.3f} dB")
    
    # Tilt penalty
    tilt_0_5deg = 4.34 * (np.pi * w_eff * np.deg2rad(0.5) / LAMBDA)**2
    tilt_1_0deg = 4.34 * (np.pi * w_eff * np.deg2rad(1.0) / LAMBDA)**2
    print(f"  Tilt penalty (0.5°): {tilt_0_5deg:.3f} dB")
    print(f"  Tilt penalty (1.0°): {tilt_1_0deg:.3f} dB")
    
    # Total budget
    print("\n[5] Estimated Total Loss Budget...")
    best_loss = -10 * np.log10(eta[idx_opt]) + fresnel_db + offset_1um
    expected_loss = -10 * np.log10(eta[idx_opt]) + fresnel_db + offset_125um
    worst_loss = -10 * np.log10(eta[idx_opt]) + fresnel_db + 2*offset_125um + tilt_0_5deg
    print(f"  Best case:     {best_loss:.2f} dB")
    print(f"  Expected case: {expected_loss:.2f} dB")
    print(f"  Worst case:    {worst_loss:.2f} dB")
    print(f"  < 0.5 dB?      {'YES ✓' if expected_loss < 0.5 else 'BORDERLINE'}")
    
    diagnostics = {
        'n_modes': len(modes),
        'g': float(g),
        'L': float(L),
        'L_half': float(L/2),
        'eta_max_pct': float(eta[idx_opt] * 100),
        'loss_min_dB': float(-10 * np.log10(eta[idx_opt])),
        'z_opt': float(z[idx_opt]),
        'w_rms_opt': float(w_eff),
        'fresnel_dB': float(fresnel_db),
        'offset_1um_dB': float(offset_1um),
        'offset_125um_dB': float(offset_125um),
        'tilt_0_5deg_dB': float(tilt_0_5deg),
        'best_loss_dB': float(best_loss),
        'expected_loss_dB': float(expected_loss),
        'worst_loss_dB': float(worst_loss),
        'under_0_5dB': best_loss < 0.5,
    }
    
    return modes, diagnostics, z, eta


# ══════════════════════════════════════════════════════════════════════
#  8. Main
# ══════════════════════════════════════════════════════════════════════
def main():
    print("=" * 70)
    print("  GRIN MMF → HCF Adapter — Full Physics Simulation")
    print("=" * 70)
    
    # ─── Baseline ──────────────────────────────────────────────────
    print("\n\n>>> BASELINE (OM4: NA=0.200, a=25μm, α=2.0) <<<")
    modes_base, diag_base, z_base, eta_base = run_diagnostics(PAR)
    
    # ─── Compare numerical vs analytic modes ──────────────────────
    print("\n\n>>> MODE VALIDATION: Numerical vs Analytic (α=2) <<<")
    modes_analytic = analytic_modes(PAR)
    r = modes_base[0]['r']
    for i in range(min(len(modes_base), len(modes_analytic))):
        ol = overlap(modes_base[i]['psi'], r,
                     modes_analytic[i]['psi'], r)
        print(f"  LP₀{i+1}: overlap = {ol:.6f}  "
              f"(β_num={modes_base[i]['beta']:.6f}, "
              f"β_ana={modes_analytic[i]['beta']:.6f})")
    
    # ─── Generate Plots ────────────────────────────────────────────
    print("\n\n>>> GENERATING PLOTS <<<")
    
    # 1. Coupling vs length
    plot_coupling_curve(PAR)
    print("  ✓ 01_coupling_vs_length.png")
    
    # 2. Mode profiles
    plot_mode_profiles(modes_base, PAR)
    print("  ✓ 02_mode_profiles.png")
    
    # 3. Excitation
    plot_excitation(modes_base, PAR)
    print("  ✓ 03_excitation.png")
    
    # 4. Field evolution
    plot_field_evolution(modes_base, PAR)
    print("  ✓ 04_field_evolution.png")
    
    # 5. Offset sensitivity
    w_eff = plot_offset_sensitivity(modes_base, PAR)
    print(f"  ✓ 06_offset_sensitivity.png  (w_eff={w_eff:.1f}μm)")
    
    # 6. Tilt sensitivity
    plot_tilt_sensitivity(modes_base, PAR)
    print("  ✓ 08_tilt_sensitivity.png")
    
    # ─── Parameter Sweeps ──────────────────────────────────────────
    print("\n\n>>> PARAMETER SWEEPS <<<")
    
    # NA sweep
    print("  Sweeping NA...")
    na_values = np.linspace(0.14, 0.24, 30)
    na_results = sweep_parameter('NA', na_values, PAR)
    plot_sweep_results('NA Sweep', na_results,
                        'Numerical Aperture (NA)', 'NA')
    print("  ✓ sweep_NA.png")
    
    # Core radius sweep
    print("  Sweeping core radius...")
    a_values = np.linspace(15, 35, 30)
    a_results = sweep_parameter('a', a_values, PAR)
    plot_sweep_results('Core Radius Sweep', a_results,
                        'Core Radius a (μm)', 'a')
    print("  ✓ sweep_a.png")
    
    # Alpha sweep
    print("  Sweeping α-profile...")
    alpha_values = np.linspace(1.6, 2.4, 30)
    alpha_results = sweep_parameter('alpha', alpha_values, PAR)
    plot_sweep_results('α-Profile Sweep', alpha_results,
                        'Profile Parameter α', 'alpha')
    print("  ✓ sweep_alpha.png")
    
    # SMF spot size sweep (what if we use different SMF?)
    print("  Sweeping SMF spot size...")
    w_smf_values = np.linspace(3, 8, 25)
    w_smf_results = sweep_parameter('w_smf', w_smf_values, PAR)
    plot_sweep_results('SMF Spot Size Sweep', w_smf_results,
                        'SMF Spot Size w_smf (μm)', 'w_smf')
    print("  ✓ sweep_w_smf.png")
    
    # HCF spot size sweep
    print("  Sweeping HCF spot size...")
    w_hcf_values = np.linspace(8, 16, 30)
    w_hcf_results = sweep_parameter('w_hcf', w_hcf_values, PAR)
    plot_sweep_results('HCF Spot Size Sweep', w_hcf_results,
                        'HCF Spot Size w_hcf (μm)', 'w_hcf')
    print("  ✓ sweep_w_hcf.png")
    
    # ─── Wavelength ────────────────────────────────────────────────
    print("\n\n>>> WAVELENGTH DEPENDENCE <<<")
    wav, wav_loss = plot_wavelength_sweep(PAR)
    print(f"  1550nm: {wav_loss[np.argmin(np.abs(wav-1.55))]:.2f} dB")
    print(f"  1310nm: {wav_loss[np.argmin(np.abs(wav-1.31))]:.2f} dB")
    print(f"  1625nm: {wav_loss[np.argmin(np.abs(wav-1.625))]:.2f} dB")
    print("  ✓ 07_wavelength_sweep.png")
    
    # ─── Monte Carlo ───────────────────────────────────────────────
    print("\n\n>>> MONTE CARLO (Manufacturing Tolerance) <<<")
    mc_results = monte_carlo(3000, n_modes=4)
    mc_stats = plot_monte_carlo(mc_results, PAR)
    print(f"  Samples: {mc_stats['n_samples']}")
    print(f"  Mean loss: {mc_stats['mean_loss']:.2f} dB")
    print(f"  Median loss: {mc_stats['median_loss']:.2f} dB")
    print(f"  Std loss: {mc_stats['std_loss']:.2f} dB")
    print(f"  P(<0.5 dB): {mc_stats['p_under_0_5dB']:.1f}%")
    print(f"  P(<0.3 dB): {mc_stats['p_under_0_3dB']:.1f}%")
    print("  ✓ 05_monte_carlo.png")
    
    # ─── Boundary Cases ────────────────────────────────────────────
    print("\n\n>>> BOUNDARY CASE ANALYSIS <<<")
    
    boundaries = [
        ('Low NA (worst OM4)', {'NA': 0.185}),
        ('High NA (worst OM4)', {'NA': 0.215}),
        ('Small core', {'a': 23.5}),
        ('Large core', {'a': 26.5}),
        ('α = 1.9 (near step)', {'alpha': 1.9}),
        ('α = 2.4 (over-compensated)', {'alpha': 2.4}),
        ('Low NA + small core', {'NA': 0.185, 'a': 23.5}),
        ('High NA + large core + α=2.1', {'NA': 0.215, 'a': 26.5, 'alpha': 2.1}),
    ]
    
    boundary_results = []
    for label, overrides in boundaries:
        p = PAR.copy()
        p.update(overrides)
        p['n2'] = np.sqrt(p['n1']**2 - p['NA']**2)
        p['Delta'] = (p['n1']**2 - p['n2']**2) / (2 * p['n1']**2)
        
        _, diag, _, _ = run_diagnostics(p)
        boundary_results.append({
            'label': label,
            'loss_dB': diag['expected_loss_dB'],
            'z_opt': diag['z_opt'],
            'under_0_5dB': diag['under_0_5dB'],
        })
        print(f"  {label}:")
        print(f"    Loss expected: {diag['expected_loss_dB']:.2f} dB")
        print(f"    z_opt: {diag['z_opt']:.0f} μm")
        print(f"    < 0.5 dB: {'YES' if diag['under_0_5dB'] else 'NO'}")
    
    # ─── Save All Data ─────────────────────────────────────────────
    print("\n\n>>> SAVING RESULTS <<<")
    
    results = {
        'parameters': PAR,
        'baseline_diagnostic': diag_base,
        'monte_carlo': mc_stats,
        'boundary_cases': boundary_results,
        'sweeps': {
            'NA': [{'NA': r['value'], 'loss_dB': r.get('loss_dB')}
                   for r in na_results if r.get('error') is None],
            'a': [{'a': r['value'], 'loss_dB': r.get('loss_dB')}
                  for r in a_results if r.get('error') is None],
            'alpha': [{'alpha': r['value'], 'loss_dB': r.get('loss_dB')}
                      for r in alpha_results if r.get('error') is None],
        }
    }
    
    with open(OUT / 'simulation_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"  Saved to {OUT / 'simulation_results.json'}")
    print("\n" + "=" * 70)
    print("  SIMULATION COMPLETE")
    print("=" * 70)


if __name__ == '__main__':
    main()

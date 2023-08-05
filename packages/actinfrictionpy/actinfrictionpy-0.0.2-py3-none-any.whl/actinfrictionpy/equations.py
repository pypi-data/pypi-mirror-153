"""Implementation of overdamped equations of motion."""

import collections
import math

from scipy import constants


ParamsRing = collections.namedtuple(
    "ParamsRing",
    [
        "r01",
        "r10",
        "r12",
        "r21",
        "deltas",
        "deltad",
        "k",
        "T",
        "Nf",
        "Nsca",
        "EI",
        "Lf",
        "zeta0",
        "KsD",
        "KdD",
        "cX",
    ],
)


ParamsLinear = collections.namedtuple(
    "ParamsLinear",
    [
        "r01",
        "r10",
        "r12",
        "r21",
        "deltas",
        "deltad",
        "k",
        "T",
        "zeta0",
        "Fcond",
    ],
)


def equation_of_motion_linear(t, lmbda, p):
    zs = p.r01 / p.r10
    zd = p.r01 * p.r12 / (p.r10 * p.r21)
    z = zd / (1 + zs) ** 2
    rhos = (zs + zs**2) / ((1 + zs) ** 2 + zd)
    rhod = z / (1 + z)
    B = p.k * p.deltas**2 / (8 * constants.k * p.T) - math.log(2)
    b = (z + 1) / (z * math.exp(-B * math.exp((rhod + rhos) / (4 * B))) + 1)
    a = p.Fcond / (p.deltas * p.zeta0 * b)
    return a / b ** (p.deltas / p.deltad * lmbda)


def equation_of_motion_ring(t, lmbda, p):
    zs = p.r01 / p.r10
    zd = p.r01 * p.r12 / (p.r10 * p.r21)
    z = zd / (1 + zs) ** 2
    rhos = (zs + zs**2) / ((1 + zs) ** 2 + zd)
    rhod = z / (1 + z)
    B = p.k * p.deltas**2 / (8 * constants.k * p.T) - math.log(2)
    C = (z + 1) / (z * math.exp(-B * math.exp((rhod + rhos) / (4 * B))) + 1)
    A = 1 / (p.deltas * p.zeta0 * (2 * p.Nf - p.Nsca)) * C ** (p.Nsca - 2 * p.Nf)
    D = p.deltas / p.deltad * (2 * p.Nf - p.Nsca)
    F = 8 * math.pi**3 * p.EI * p.Lf * p.Nf / p.Nsca**3
    G = -(p.deltas**3)
    H = 3 * p.Lf * p.deltas**2
    J = -3 * p.Lf**2 * p.deltas
    K = p.Lf**3
    M = (
        -2
        * math.pi
        * constants.k
        * p.T
        * (2 * p.Nf - p.Nsca)
        / (p.Nsca * p.deltad)
        * math.log(1 + p.KsD**2 * p.cX / (p.KdD * (p.KsD + p.cX) ** 2))
    )

    return (
        -A
        * C ** (-D * lmbda)
        * (F / (G * lmbda**3 + H * lmbda**2 + J * lmbda + K) + M)
    )


def bending_force(lmbda, p):
    F = 8 * math.pi**3 * p.EI * p.Lf * p.Nf / p.Nsca**3
    G = -(p.deltas**3)
    H = 3 * p.Lf * p.deltas**2
    J = -3 * p.Lf**2 * p.deltas
    K = p.Lf**3

    return F / (G * lmbda**3 + H * lmbda**2 + J * lmbda + K)


def total_force(lmbda, p):
    M = (
        -2
        * math.pi
        * constants.k
        * p.T
        * (2 * p.Nf - p.Nsca)
        / (p.Nsca * p.deltad)
        * math.log(1 + p.KsD**2 * p.cX / (p.KdD * (p.KsD + p.cX) ** 2))
    )

    return bending_force(lmbda, p) + M


def condensation_force(p):
    M = (
        -2
        * math.pi
        * constants.k
        * p.T
        * (2 * p.Nf - p.Nsca)
        / (p.Nsca * p.deltad)
        * math.log(1 + p.KsD**2 * p.cX / (p.KdD * (p.KsD + p.cX) ** 2))
    )

    return M


def friction_coefficient_linear(lmbda, p):
    zs = p.r01 / p.r10
    zd = p.r01 * p.r12 / (p.r10 * p.r21)
    z = zd / (1 + zs) ** 2
    rhos = (zs + zs**2) / ((1 + zs) ** 2 + zd)
    rhod = z / (1 + z)
    B = p.k * p.deltas**2 / (8 * constants.k * p.T) - math.log(2)
    C = (z + 1) / (z * math.exp(-B * math.exp((rhod + rhos) / (4 * B))) + 1)

    return p.zeta0 * C ** (1 + p.deltas / p.deltad * lmbda)


def friction_coefficient_ring(lmbda, p):
    zs = p.r01 / p.r10
    zd = p.r01 * p.r12 / (p.r10 * p.r21)
    z = zd / (1 + zs) ** 2
    rhos = (zs + zs**2) / ((1 + zs) ** 2 + zd)
    rhod = z / (1 + z)
    B = p.k * p.deltas**2 / (8 * constants.k * p.T) - math.log(2)
    C = (z + 1) / (z * math.exp(-B * math.exp((rhod + rhos) / (4 * B))) + 1)

    return p.zeta0 * C ** ((1 + p.deltas / p.deltad * lmbda) * (2 * p.Nf - p.Nsca))


def calc_equilibrium_ring_radius(p) -> float:
    """Calculate the equilibrium radius of a ring analytically."""
    num = p.EI * p.Nf * p.deltad * p.Lf * p.Nsca
    denom = (
        2
        * math.pi
        * p.T
        * constants.k
        * math.log(1 + p.KsD**2 * p.cX / (p.KdD * (p.KsD + p.cX) ** 2))
        * (2 * p.Nf - p.Nsca)
    )

    return (num / denom) ** (1 / 3)

// ============================================================
// Financial engines test suite — feasibility-study-app
// Tests for: src/lib/calculations.ts, src/lib/advanced-finance.ts,
//            src/lib/monte-carlo.ts
// Pure TypeScript — no external deps. Run with: bun test
// ============================================================
import { describe, test, expect } from 'bun:test';

import {
  calculateNPV,
  calculateIRR,
  calculatePayback,
  calculateROI,
  calculatePI,
  calculateMIRR,
  calculateDiscountedPayback,
  calculateWACC,
  calcNetCashFlow,
  calculateIndicators,
} from '../src/lib/calculations';

import {
  calculateAmortization,
  calculateTaxes,
  runScenarioAnalysis,
  calculateTornado,
  DEFAULT_SCENARIOS,
} from '../src/lib/advanced-finance';

import { runMonteCarlo } from '../src/lib/monte-carlo';

// ---------- shared fixtures ----------
const CF_SIMPLE = [-100, 60, 60];          // classic 2-year recovery
const RATE = 10;

// ============================================================
// 1) calculations.ts — core indicators
// ============================================================
describe('calculateNPV', () => {
  test('known analytic value (r=10%)', () => {
    // -100 + 60/1.1 + 60/1.21 = 4.13223...
    expect(calculateNPV(CF_SIMPLE, RATE)).toBeCloseTo(4.13223, 3);
  });

  test('zero rate reduces to simple sum', () => {
    expect(calculateNPV(CF_SIMPLE, 0)).toBe(20);
  });

  test('empty flows return 0', () => {
    expect(calculateNPV([], 10)).toBe(0);
  });

  test('higher rate lowers NPV for positive-tail flows', () => {
    const low = calculateNPV(CF_SIMPLE, 5);
    const high = calculateNPV(CF_SIMPLE, 20);
    expect(low).toBeGreaterThan(high);
  });
});

describe('calculateIRR', () => {
  test('exact root for [-100, 110] = 10%', () => {
    expect(calculateIRR([-100, 110]) as number).toBeCloseTo(10, 3);
  });

  test('root for [-100, 60, 60] and NPV(IRR)≈0', () => {
    const irr = calculateIRR(CF_SIMPLE) as number;
    expect(irr).toBeCloseTo(13.0646, 2);
    expect(calculateNPV(CF_SIMPLE, irr)).toBeCloseTo(0, 4);
  });

  test('no sign change returns null', () => {
    expect(calculateIRR([50, 60, 70])).toBeNull();
    expect(calculateIRR([-100, -50])).toBeNull();
  });

  test('too few flows returns null', () => {
    expect(calculateIRR([-100])).toBeNull();
    expect(calculateIRR([])).toBeNull();
  });
});

describe('calculatePayback', () => {
  test('crossing mid-year: [-100, 60, 60] → 1.6667', () => {
    expect(calculatePayback(CF_SIMPLE) as number).toBeCloseTo(1.66667, 3);
  });

  test('[-100, 30, 30, 30, 30] → 3.3333', () => {
    expect(calculatePayback([-100, 30, 30, 30, 30]) as number).toBeCloseTo(3.33333, 3);
  });

  test('never recovers → null', () => {
    expect(calculatePayback([-100, 10, 10])).toBeNull();
  });
});

describe('calculateROI / calculatePI', () => {
  test('ROI percent', () => {
    expect(calculateROI(60, 100)).toBe(60);
    expect(calculateROI(60, 0)).toBe(0);
  });

  test('PI = PV(future)/initial', () => {
    expect(calculatePI(CF_SIMPLE, RATE)).toBeCloseTo(1.041322, 3);
  });
});

describe('calculateMIRR (after indexOf fix)', () => {
  test('[-100, 110] finance=0 reinvest=0 → 10%', () => {
    // fv = 110, pv = -100, n = 1 → (110/100)^(1/1) - 1 = 10%
    expect(calculateMIRR([-100, 110], 0, 0) as number).toBeCloseTo(10, 4);
  });

  test('duplicate cash flows no longer double-count years', () => {
    // [-100, 50, 50]: fv = 50*1.1 + 50*1.1^0 = 105 (not 110)
    // MIRR = (105/100)^(1/2) - 1 = 2.4695%
    expect(calculateMIRR([-100, 50, 50], 10, 10) as number).toBeCloseTo(2.4695, 3);
  });

  test('missing sign change returns null', () => {
    expect(calculateMIRR([10, 20], 10, 10)).toBeNull();
  });
});

describe('calculateDiscountedPayback', () => {
  test('[-100, 60, 60] at 10% → 1.9167', () => {
    // cum: -100, -45.4545, +4.1322 → cross at i=2: fraction 0.91667 → 1 + 0.91667
    expect(calculateDiscountedPayback(CF_SIMPLE, RATE) as number).toBeCloseTo(1.91667, 3);
  });
});

describe('calculateWACC', () => {
  test('weighted average with tax shield', () => {
    // 0.6*15 + 0.4*10*(1-0.15) = 9 + 3.4 = 12.4
    expect(calculateWACC(600, 400, 15, 10, 0.15)).toBeCloseTo(12.4, 6);
  });

  test('zero capital → 0', () => {
    expect(calculateWACC(0, 0, 15, 10)).toBe(0);
  });
});

describe('calcNetCashFlow', () => {
  test('revenues minus costs with NaN safety', () => {
    expect(calcNetCashFlow({ year: 1, revenues: 500, costs: 200 })).toBe(300);
    expect(calcNetCashFlow({ year: 1, revenues: NaN, costs: 200 })).toBe(-200);
  });
});

describe('calculateIndicators — integration', () => {
  const viable = calculateIndicators({
    initialInvestment: 1000,
    discountRate: 10,
    yearsData: [
      { year: 1, revenues: 900, costs: 400 },
      { year: 2, revenues: 900, costs: 400 },
      { year: 3, revenues: 900, costs: 400 },
    ],
  });

  test('viability flags on NPV>0 and IRR>rate', () => {
    expect(viable.npv).toBeCloseTo(243.426, 2);
    expect(viable.irr as number).toBeGreaterThan(10);
    expect(viable.isViable).toBe(true);
  });

  test('structure: year 0 = -investment, cumulative ends positive', () => {
    expect(viable.netCashFlows[0]).toBe(-1000);
    expect(viable.netCashFlows.length).toBe(4);
    expect(viable.cumulativeCashFlows[3]).toBeCloseTo(500, 6);
  });

  test('payback exactly 2.0 for symmetric flows', () => {
    expect(viable.paybackPeriod as number).toBeCloseTo(2.0, 4);
  });

  test('ROI = totalNetProfit/investment', () => {
    expect(viable.totalNetProfit).toBe(1500);
    expect(viable.roi).toBe(150);
    expect(viable.averageAnnualProfit).toBe(500);
  });

  test('unviable project flags false', () => {
    const bad = calculateIndicators({
      initialInvestment: 1000,
      discountRate: 10,
      yearsData: [
        { year: 1, revenues: 500, costs: 400 },
        { year: 2, revenues: 500, costs: 400 },
        { year: 3, revenues: 500, costs: 400 },
      ],
    });
    expect(bad.npv).toBeLessThan(0);
    expect(bad.isViable).toBe(false);
  });
});

// ============================================================
// 2) advanced-finance.ts — amortization, taxes, scenarios, tornado
// ============================================================
describe('calculateAmortization', () => {
  const am = calculateAmortization(100000, 12, 1); // 12% annual, 1 year

  test('monthly payment matches annuity formula', () => {
    // PMT = 100000*0.01*(1.01^12)/((1.01^12)-1) ≈ 8884.88
    expect(am.monthlyPayment).toBeCloseTo(8884.88, 1);
  });

  test('schedule integrity: 12 rows, final balance ~0, principal fully repaid', () => {
    expect(am.schedule.length).toBe(12);
    // float residual ~1e-10 YER is immaterial → assert to 6 decimals (micro-YER)
    expect(am.schedule[11].balance).toBeCloseTo(0, 6);
    expect(am.schedule[11].cumulativePrincipal).toBeCloseTo(100000, 4);
  });

  test('totals: totalPayment = PMT*12, totalInterest = payments - principal', () => {
    expect(am.totalPayment).toBeCloseTo(am.monthlyPayment * 12, 4);
    expect(am.totalInterest).toBeCloseTo(am.monthlyPayment * 12 - 100000, 4);
    const sumInterest = am.schedule.reduce((s, r) => s + r.interest, 0);
    expect(sumInterest).toBeCloseTo(am.totalInterest, 2);
  });

  test('yearly summary aggregates correctly', () => {
    expect(am.yearlySummary.length).toBe(1);
    expect(am.yearlySummary[0].payment).toBeCloseTo(am.monthlyPayment * 12, 4);
    expect(am.yearlySummary[0].balanceEnd).toBeCloseTo(0, 6);
  });

  test('zero-interest loan pays principal evenly', () => {
    const zero = calculateAmortization(12000, 0, 1);
    expect(zero.monthlyPayment).toBe(1000);
    expect(zero.totalInterest).toBe(0);
  });

  test('invalid inputs short-circuit safely', () => {
    const bad = calculateAmortization(0, 12, 5);
    expect(bad.schedule.length).toBe(0);
    expect(bad.monthlyPayment).toBe(0);
  });
});

describe('calculateTaxes', () => {
  const t = calculateTaxes(100000, 60000, 5, 15, 0.7);

  test('VAT split: on sales, deductible on purchases, net payable', () => {
    expect(t.vatOnSales).toBeCloseTo(4761.9048, 3);
    expect(t.vatOnPurchases).toBeCloseTo(2000.0, 3);
    expect(t.vatNetPayable).toBeCloseTo(2761.9048, 3);
  });

  test('income tax on positive profit only', () => {
    expect(t.taxableIncome).toBe(40000);
    expect(t.incomeTax).toBe(6000);
    expect(t.netProfitAfterTax).toBe(34000);
  });

  test('effective rate blends VAT + income tax', () => {
    expect(t.effectiveTaxRate).toBeCloseTo(21.9048, 3);
  });

  test('loss case: no income tax, profit stays negative', () => {
    const loss = calculateTaxes(50000, 80000, 5, 15, 0.7);
    expect(loss.taxableIncome).toBe(0);
    expect(loss.incomeTax).toBe(0);
    expect(loss.netProfitAfterTax).toBe(-30000);
  });
});

describe('runScenarioAnalysis', () => {
  const years = [
    { year: 1, revenues: 900, costs: 400 },
    { year: 2, revenues: 900, costs: 400 },
    { year: 3, revenues: 900, costs: 400 },
  ];
  const analysis = runScenarioAnalysis(
    1000, years, 10, DEFAULT_SCENARIOS, calculateNPV, calculateIRR
  );

  test('three scenarios evaluated with adjusted flows', () => {
    expect(analysis.results.length).toBe(3);
    const realistic = analysis.results.find((r) => r.scenario.nameEn === 'Realistic')!;
    expect(realistic.npv).toBeCloseTo(243.426, 2);
    expect(realistic.totalRevenues).toBeCloseTo(2700, 6);
  });

  test('best/worst/base identification', () => {
    expect(analysis.bestCase!.scenario.nameEn).toBe('Optimistic');
    expect(analysis.worstCase!.scenario.nameEn).toBe('Pessimistic');
    expect(analysis.baseCase!.scenario.nameEn).toBe('Realistic');
    expect(analysis.bestCase!.npv).toBeGreaterThan(analysis.worstCase!.npv);
  });

  test('probability-weighted NPV and risk premium', () => {
    // 0.25*optimistic + 0.5*realistic + 0.25*pessimistic
    const opt = analysis.bestCase!.npv, pes = analysis.worstCase!.npv, base = analysis.baseCase!.npv;
    const expectedWeighted = 0.25 * opt + 0.5 * base + 0.25 * pes;
    expect(analysis.weightedNPV).toBeCloseTo(expectedWeighted, 6);
    expect(analysis.expectedValue).toBe(analysis.weightedNPV);
    expect(analysis.riskPremium).toBeCloseTo(base - analysis.weightedNPV, 6);
    expect(analysis.range).toBeCloseTo(opt - pes, 6);
  });
});

describe('calculateTornado', () => {
  const base = {
    initialInvestment: 1000,
    revenues: [500, 500, 500],
    costs: [200, 200, 200],
    discountRate: 10,
  };
  const variations = [
    { variable: 'revenues', variableAr: 'الإيرادات', lowFactor: 0.8, highFactor: 1.2 },
    { variable: 'costs', variableAr: 'التكاليف', lowFactor: 0.9, highFactor: 1.1 },
    { variable: 'discountRate', variableAr: 'معدل الخصم', lowFactor: 0.9, highFactor: 1.1 },
  ];
  const items = calculateTornado(base, calculateNPV, variations);

  test('returns items sorted by swing (descending)', () => {
    expect(items.length).toBe(3);
    for (let i = 1; i < items.length; i++) {
      expect(items[i - 1].swing).toBeGreaterThanOrEqual(items[i].swing);
    }
    expect(items[0].variable).toBe('revenues');
  });

  test('highest-impact variable normalized to 100%', () => {
    expect(items[0].impact).toBeCloseTo(100, 6);
    items.forEach((it) => expect(it.impact).toBeLessThanOrEqual(100.0001));
  });

  test('low/high values ordered correctly for flow variables', () => {
    const rev = items.find((i) => i.variable === 'revenues')!;
    expect(rev.lowValue).toBeLessThan(rev.highValue);
    expect(rev.baseValue).toBeCloseTo(calculateNPV([-1000, 300, 300, 300], 10), 6);
  });

  test('discount-rate branch inverts rate effect (higher rate → lower NPV)', () => {
    const dr = items.find((i) => i.variable === 'discountRate')!;
    expect(dr.lowValue).toBeLessThan(dr.highValue);
  });
});

// ============================================================
// 3) monte-carlo.ts — deterministic + statistical invariants
// ============================================================
describe('runMonteCarlo', () => {
  const baseInputs = {
    initialInvestment: 1000,
    yearsData: [
      { year: 1, revenues: 900, costs: 400 },
      { year: 2, revenues: 900, costs: 400 },
      { year: 3, revenues: 900, costs: 400 },
    ],
    discountRate: 10,
  };

  test('zero volatility degenerates to deterministic NPV', () => {
    const res = runMonteCarlo({ ...baseInputs, revenueVolatility: 0, costVolatility: 0, iterations: 500 });
    // every trial identical → mean/min/max/percentiles all equal analytic NPV
    const analytic = calculateNPV([-1000, 500, 500, 500], 10);
    expect(res.npvMean).toBeCloseTo(analytic, 6);
    expect(res.npvStd).toBeCloseTo(0, 6);
    expect(res.npvMin).toBeCloseTo(res.npvMax, 6);
    expect(res.npvP5).toBeCloseTo(analytic, 6);
    expect(res.probNPVPositive).toBe(1);
    expect(res.riskAdjustedNPV).toBeCloseTo(analytic, 6);
  });

  test('risk metrics are internally consistent', () => {
    const res = runMonteCarlo({ ...baseInputs, revenueVolatility: 0.2, costVolatility: 0.1, iterations: 2000 });
    expect(res.var95).toBe(res.npvP5);
    expect(res.cvar95).toBe(res.expectedShortfall);
    expect(res.riskAdjustedNPV).toBeCloseTo(res.npvMean - 1.65 * res.npvStd, 6);
  });

  test('statistical ordering of percentiles and bounds', () => {
    const res = runMonteCarlo({ ...baseInputs, revenueVolatility: 0.2, costVolatility: 0.1, iterations: 2000 });
    expect(res.npvP5).toBeLessThanOrEqual(res.npvP25);
    expect(res.npvP25).toBeLessThanOrEqual(res.npvP75);
    expect(res.npvP75).toBeLessThanOrEqual(res.npvP95);
    expect(res.npvMin).toBeLessThanOrEqual(res.npvMean);
    expect(res.npvMean).toBeLessThanOrEqual(res.npvMax);
    expect(res.expectedShortfall).toBeLessThanOrEqual(res.npvMean);
    expect(res.probNPVPositive).toBeGreaterThanOrEqual(0);
    expect(res.probNPVPositive).toBeLessThanOrEqual(1);
  });

  test('distribution has 20 bins within iteration bounds', () => {
    const res = runMonteCarlo({ ...baseInputs, revenueVolatility: 0.2, costVolatility: 0.1, iterations: 1000 });
    expect(res.distribution.length).toBe(20);
    const total = res.distribution.reduce((s, b) => s + b.count, 0);
    expect(total).toBeLessThanOrEqual(1000); // max value excluded by v < binEnd
  });

  test('sample paths start at -investment and capped at 50', () => {
    const res = runMonteCarlo({ ...baseInputs, revenueVolatility: 0.2, costVolatility: 0.1, iterations: 300 });
    expect(res.samplePaths.length).toBe(50);
    res.samplePaths.forEach((p) => {
      expect(p[0]).toBe(-1000);
      expect(p.length).toBe(4); // t0 + 3 years
    });
  });

  test('statistical mean stays near analytic base case (loose band)', () => {
    const res = runMonteCarlo({ ...baseInputs, revenueVolatility: 0.2, costVolatility: 0.1, iterations: 2000 });
    expect(Math.abs(res.npvMean - 243.426)).toBeLessThan(150);
  });
});

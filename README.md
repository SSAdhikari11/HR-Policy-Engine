





<h1 align="center">HR Policy Engine</h1>

<p align="center">
  Advanced HR Rule Automation for ERPNext & Frappe
</p>

<p align="center">
  Automate attendance policies, leave deductions, payroll deductions,
  sandwich rules, working-hour compliance, and custom HR governance.
</p>

<hr>

<h2>Overview</h2>

<p>
HR Policy Engine is a custom Frappe/ERPNext application that enables organizations
to define and enforce HR policies that are not available out-of-the-box.
</p>

<p>
The system automatically evaluates attendance, leave applications,
working hours, late arrivals, and early exits to determine whether
deductions should be applied to leave balances or payroll.
</p>

<hr>

<h2>Core Features</h2>

<ul>
  <li>Configurable HR Policy Rules</li>
  <li>Automatic Leave Deductions</li>
  <li>Automatic Payroll Deductions</li>
  <li>Attendance Compliance Monitoring</li>
  <li>Policy Priority Engine</li>
  <li>Leave & Payroll Audit Logs</li>
</ul>

<hr>

<h2>Supported Rules</h2>

<h3>1. Sandwich Rule</h3>

<p>
If an employee applies leave before and after holidays/weekends,
the intervening holidays can also be counted as leave.
</p>

<p><b>Example:</b></p>

<pre>
Friday     = Leave
Saturday   = Holiday
Sunday     = Holiday
Monday     = Leave

Result:
Saturday and Sunday are also counted as leave.
</pre>

<p>
🎥 Demo:
<a href="YOUR_VIDEO_LINK_HERE](https://github.com/user-attachments/assets/3a8260ba-880f-49f1-b450-2cdae15a5d20">Watch Demo</a>
</p>

<hr>

<h3>2. Late Entry Count Rule</h3>

<p>
Defines how many late entries are allowed before deductions begin.
</p>

<pre>
Allowed Late Entries: 3

1st Late Entry  -> Allowed
2nd Late Entry  -> Allowed
3rd Late Entry  -> Allowed
4th Late Entry  -> Deduction Applied
</pre>

<p>
🎥 Demo:
<a href="#">Coming Soon</a>
</p>

<hr>

<h3>3. Early Exit Count Rule</h3>

<p>
Defines how many early exits are allowed before deductions begin.
</p>

<pre>
Allowed Early Exits: 2

1st Exit -> Allowed
2nd Exit -> Allowed
3rd Exit -> Deduction Applied
</pre>

<p>
🎥 Demo:
<a href="#">Coming Soon</a>
</p>

<hr>

<h3>4. Daily Hours Fulfillment Rule</h3>

<p>
Employees who complete the required working hours are protected
from late-entry and early-exit penalties.
</p>

<pre>
Required Hours: 9

Check-In: 10:00 AM
Check-Out: 07:00 PM

Worked Hours: 9

Result:
No violation recorded.
</pre>

<p>
🎥 Demo:
<a href="#">Coming Soon</a>
</p>

<hr>

<h3>5. Monthly Late Time Allowance</h3>

<p>
Allows employees to accumulate a fixed amount of late minutes
during a month before deductions begin.
</p>

<pre>
Monthly Allowance: 60 Minutes

Late by 15 mins × 4 times

Total = 60 Minutes

Result:
No deduction

61st minute onward:
Deduction starts.
</pre>

<p>
🎥 Demo:
<a href="#">Coming Soon</a>
</p>

<hr>

<h2>Rule Priority Engine</h2>

<p>
The system evaluates rules using the following priority:
</p>

<ol>
  <li>Daily Hours Fulfillment</li>
  <li>Monthly Late Time Allowance</li>
  <li>Late Entry Count</li>
  <li>Early Exit Count</li>
  <li>Sandwich Rule</li>
</ol>

<p>
Daily Hours Fulfillment has the highest priority and can override
late-entry and early-exit violations if required working hours
are completed.
</p>

<hr>

<h2>Deduction Modes</h2>

<h3>Leave Balance Deduction</h3>

<ul>
  <li>Reduces available leave balance.</li>
  <li>Supports leave priority logic.</li>
  <li>Creates Leave Deduction Logs.</li>
</ul>

<h3>Payroll Deduction</h3>

<ul>
  <li>Deducts directly from payroll.</li>
  <li>Creates Payroll Deduction Logs.</li>
  <li>Updates Salary Slip calculations.</li>
</ul>

<hr>

<h2>Screenshots</h2>

<h3>HR Policy Configuration</h3>

<img src="screenshots/hr-policy-engine.png" width="900">

<hr>

<h2>Technology Stack</h2>

<ul>
  <li>Frappe Framework</li>
  <li>ERPNext</li>
  <li>Python</li>
  <li>MariaDB</li>
  <li>JavaScript</li>
</ul>

<hr>

<h2>Installation</h2>

<pre>
bench get-app https://github.com/SSAdhikari11/hr_policy_engine.git

bench --site your-site install-app hr_policy_engine
</pre>

<hr>

<h2>Author</h2>

<p>
Developed by Suraj using Frappe Framework & ERPNext.
</p>

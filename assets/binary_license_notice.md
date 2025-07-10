> ## 📄 License Notice for Binary Distributions
>
> The **compiled executable binaries** provided in the [Releases section](https://github.com/AlinaWan/pip-reroller/releases) are distributed as a convenience for end users. These binaries constitute a collective work that includes both original code developed under this project and third-party components subject to distinct open-source licenses. The applicable licensing terms for all included components are outlined below:
>
> ---
>
> ### ▸ Included Components and Applicable Licenses
>
> * **AutoHotkey.exe**
>   Bundled to support automation features within the application. This binary is licensed under the [GNU General Public License, Version 2 or any later version (GPLv2+)](/assets/AutoHotkey.exe.LICENSE), a strong copyleft license that imposes source disclosure and licensing obligations on derivative and collective works.
>
> * **Python Interpreter (CPython)**
>   The embedded Python runtime is licensed under the [Python Software Foundation License, Version 2 (PSFL-2.0)](/assets/python.LICENSE), which is a permissive open-source license allowing redistribution under minimal conditions.
>
> * **Python Package Dependencies (pip packages)**
>   The application statically or dynamically links against various third-party Python packages, each governed by its own license. A full inventory of these dependencies and their corresponding licenses is provided in [pip\_dependencies.LICENSE](/assets/pip_dependencies.LICENSE).
>
> * **LGPLv3-Licensed Component(s)**
>   At least one of the included Python dependencies is licensed under the [GNU Lesser General Public License, Version 3 (LGPLv3)](/assets/LGPLv3.LICENSE). While the LGPL permits dynamic linking under less restrictive terms, when combined with GPLv2+ components, the resulting binary distribution is subject to the stricter terms of the GPLv3, due to license compatibility requirements.
>
> ---
>
> ### ▸ Licensing of Source Code vs. Binary Distributions
>
> The **original source code** for this project is authored and published under the **[MIT License](/LICENSE)**, a permissive license that permits use, modification, and redistribution with minimal obligations, provided attribution and license text are preserved.
>
> However, it is important to distinguish between:
>
> 1. **The original source code**, which is independently MIT-licensed, and
> 2. **The compiled binary distribution**, which includes and redistributes third-party components that are subject to more restrictive licensing terms.
>
> When distributing the application in **binary form**, the resulting executable is no longer composed solely of the MIT-licensed source code. It constitutes a **collective or derivative work** that embeds:
>
> * A **GPLv2+ licensed binary** (AutoHotkey.exe),
> * One or more **LGPLv3-licensed libraries**, and
> * The **Python interpreter and pip-installed packages**, each with their own licenses.
>
> Because of the **inclusion of both GPLv2+ and LGPLv3 components**, and due to the legal principle of license compatibility (specifically, the upward compatibility of GPLv2+ to GPLv3 and the interaction between GPL and LGPL licenses), the binary distribution as a whole **must be licensed under the terms of the [GNU General Public License, Version 3 (GPLv3)](/assets/GPLv3.LICENSE)**.
>
> This requirement stems from the **copyleft provisions** of both the GPL and LGPL licenses, which impose downstream obligations including:
>
> * Distribution of **complete corresponding source code**,
> * Retention of license notices and attribution for all included components, and
> * Distribution of derivative or combined works under **GPLv3-compatible terms only**.
>
> ---
>
> ### ▸ Summary of Licensing Obligations
>
> * The **source code** of this project, when distributed independently, remains under the permissive **MIT License**.
> * Any **binary distribution** that includes GPLv2+/LGPLv3-licensed components **must be licensed under GPLv3** to satisfy the most restrictive copyleft obligations of the combined work.
> * Redistribution of such binaries triggers obligations under GPLv3, including but not limited to:
>
>   * Providing full source code (including for linked dependencies),
>   * Retaining all applicable license texts and notices, and
>   * Not imposing further restrictions beyond those allowed by the GPL.
>
> ---
>
> ### ▸ Compliance Notice for Redistributors
>
> If you intend to redistribute modified or unmodified copies of this application in **binary form**, you are **legally required** to:
>
> * Comply with the terms of the **GNU General Public License, Version 3**, and
> * Review and honor the licenses of all third-party dependencies included in your distribution.
>
> Failure to comply with these terms may result in a violation of the licensing agreements of the respective copyright holders.
>
> For more information on open-source license compatibility and copyleft obligations, consult the Free Software Foundation or qualified legal counsel.

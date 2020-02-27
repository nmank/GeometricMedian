function [ F, coh ] = troppaltproj_sp( n, K, d, mu )
% Alternating projection from "Constructing Packings in Grassmannian Manifolds
% via Alternating Projection"
% by I. S. Dhillon, R. W. Heath Jr., T. Strohmer, and J. A. Tropp and
% Tropp's dissertation "Topics in Sparse Approximation."

% Actual Matlab commands mainly based on code from Dustin Mixon's 
% implementation of the similar algorithm for line packing.

% Inputs:
% n = number of subspaces
% K = dimension of subpaces
% d = ambient dimension
% mu = desired "subspace coherence" (max tr P_i P_j)
%       Use 1-(d-K)*n/(d*(n-1)) for spectral distance, equiisoclinic
%       Use K*(1-(d-K)*n/(d*(n-1))) for chodal distance, equichordal

% Outputs:
% F = synthesis matrix of the ONBs of the subspace packing
% coh = resutling "subspace coherence" (max tr P_i P_j)

% Emily J. King
% August 18, 2018


% Initialize subspaces (modification of Alg 7.4 in Tropp's thesis)
tau=0.9*sqrt(K);
T=10000;
done=0;
while done == 0
    X=randSubsp(d,K)+1i*randSubsp(d,K);
    t=0;
    while t<T
        x=randSubsp(d,K)+1i*randSubsp(d,K);
        %cor=max(vecnorm(reshape(x'*X,K^2,round(size(X,2)/K)),2,1)); %my
        %old Matlab does not have vecnorm
        cor=max(sqrt(sum(reshape(x'*X,K^2,round(size(X,2)/K)).^2,1)));
        if cor<tau
            X(:,(end+1):(end+K))=x;
            t=0;
            if round(size(X,2)/K)==n
                t=T;
            end
        else
            t=t+1;
        end
    end
    if round(size(X,2)/K)==n
        done=1;
    end
end

% Alternating Projections (modification of Algorithm 7.1 in Tropp's thesis)
G=X'*X;
T=30000; % for subspace packings
%T=10000;
for t=1:T
    % project onto H(mu) by Proposition 7.7 
    for ii=1:n
        for jj=1:n
            if ii==jj
                G((1+(ii-1)*K):ii*K,(1+(jj-1)*K):jj*K)=eye(K);
                % Chordal distance (encourages equichordal)
            elseif norm(G((1+(ii-1)*K):ii*K,(1+(jj-1)*K):jj*K),'fro')>sqrt(mu)
                G((1+(ii-1)*K):ii*K,(1+(jj-1)*K):jj*K)=...
                    G((1+(ii-1)*K):ii*K,(1+(jj-1)*K):jj*K)/...
                    norm(G((1+(ii-1)*K):ii*K,(1+(jj-1)*K):jj*K),'fro')*sqrt(mu);
                % Spectral distance (encourages equiisoclinic)
%                 elseif norm(G((1+(ii-1)*K):ii*K,(1+(jj-1)*K):jj*K),2)>sqrt(mu)
%                     [U S V]=svd(G((1+(ii-1)*K):ii*K,(1+(jj-1)*K):jj*K));
%                     G((1+(ii-1)*K):ii*K,(1+(jj-1)*K):jj*K)=...
%                         U*hardThresh(S,sqrt(mu))*V';
            end
        end
    end
    G=(G+G')/2;
    % project onto G by Proposition 7.3
    [V D] = eig(G);
    [dd,ind] = sort(diag(D),'descend');
    Vs = V(:,ind);
    first=dd(1:d);
    if sum(first)>n*K
        while sum(first)>n*K
            k=sum(first>0);
            gammapart=(sum(first)-n*K)/k;
            first=(first-gammapart).*((first-gammapart)>0);
        end
    else
        first=first+(n*K-sum(first))/d;
    end
    newD=zeros(size(D));
    newD(1:d,1:d)=diag(first);
    G=Vs*newD*Vs';
end

% finalize
D=diag(diag(G));
G=inv(D^(1/2))*G*inv(D^(1/2));
G=(G+G')/2;
[V D] = eig(G);
[dd,ind] = sort(diag(D),'descend');
Ds = D(ind,ind);
Vs = V(:,ind);
sqrtDs=sqrt(Ds);
Dnew=zeros(d,n*K);
Dnew(1:d,1:d)=sqrtDs(1:d,1:d);
F=Dnew*Vs';
for ii=1:n*K
    F(:,ii)=F(:,ii)/norm(F(:,ii));
end

% Subspace coherence calculation
cohs = zeros(n);
Gr=F'*F;
for ii=2:n
    for jj=1:(ii-1)
        cohs(ii,jj)=norm(Gr((1+(ii-1)*K):ii*K,(1+(jj-1)*K):jj*K),'fro')^2;
    end
end
coh=max(cohs(:));
        
end

%% Local functions
function Y = randSubsp(ambDim,subDim)
% Produces random ONB of a random subspace
    [Q,R]=qr(rand(ambDim,subDim));
    Y=Q(:,1:subDim);
end

function M=hardThresh(A,t);
% Component-wise upper hard thesholding 
    M=A;
    over=(find(M>t));
    M(over)=t;
end


